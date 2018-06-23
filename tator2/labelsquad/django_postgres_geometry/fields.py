import re
import collections
import functools

from django.core.exceptions import FieldError
from django.utils.six import with_metaclass
from django.db import models


_FLOAT_RE = r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'


def require_postgres(fn):
    """
    Decorator that checks if the target backend engine is a PostgreSQL instance
    :raises: FieldError
    """

    def wrapper(self, connection):
        engine = connection.settings_dict['ENGINE']

        if 'psycopg2' not in engine and 'postgis' not in engine:
            raise FieldError("Current database is not a PostgreSQL instance")

        return fn(self, connection)

    return wrapper


# =============================
# Point


def parse_point(s):
    # points look like (x,y)
    beginning = "("
    middle = ","
    end = ")"
    s = s[len(beginning):-len(end)]
    vals = [int(val) for val in s.split(middle)]
    return Point(vals[0], vals[1])


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, index):
        if index not in [0, 1]:
            raise ValueError("Index of a point must be 0 or 1")
        result = self.x if index == 0 else self.y
        return result

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        try:
            result = self[self.n]
            self.n += 1
            return result
        except ValueError:
            raise StopIteration


class PointField(models.Field):
    """
    A 2D point. Looks like `( x , y )` internally.
    """

    def __init__(self, *args, **kwargs):
        # Input parameters are lists of cards ('Ah', '9s', etc.)
        super().__init__(*args, **kwargs)

    def from_db_value(self, value: Point, expression, connection):
        if value is None:
            return value
        return parse_point(value)

    def to_python(self, value: Point):
        if isinstance(value, Point):
            return value

        if value is None:
            return value

        return parse_point(value)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def get_prep_value(self, value: Point):
        if value is None:
            return value
        return f"( {value.x} , {value.y} )"

    @require_postgres
    def db_type(self, connection):
        return 'point'

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs


# =============================
# Path


def parse_path(points):
    # paths look like [ ( x1 , y1 ) , ... , ( xn , yn ) ] or ( ( x1 , y1 ) , ... , ( xn , yn ) )

    # closed brackets indicate open, parentheses indicate closed
    is_open = points[0] == '['
    beginning = '['
    end = ']'
    points = points[len(beginning):-len(end)]

    coordinates = ''.join(
        [character for character in points if character not in ['(', ')']]).split(',')
    assert len(points) % 2 == 0

    doubles = []
    for coordinate_index in range(0, len(coordinates), 2):
        doubles.append(coordinates[coordinate_index:coordinate_index + 2])

    return Path([Point(int(double[0]), int(double[1])) for double in doubles], is_open)


class Path:
    def __init__(self, points, is_open):
        if len(points) < 2:
            raise ValueError("A Path needs at minimum 2 points")

        self.points = points
        self.is_open = is_open

    def __getitem__(self, index):
        if index not in range(len(self.points)):
            raise ValueError(
                f"Trying to get index {index} of a path that's only {len(self.points)} long is not allowed.")
        result = self.points[index]
        return result

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        try:
            result = self[self.n]
            self.n += 1
            return result
        except ValueError:
            raise StopIteration

    def __len__(self):
        return len(self.points)


class PathField(models.Field):
    """
    Field to store a path (a list of at least two points). Looks like `[ ( x1 , y1 ) , ... , ( xn , yn ) ]` internally
    """

    def __init__(self, *args, **kwargs):
        # Input parameters are lists of cards ('Ah', '9s', etc.)
        super().__init__(*args, **kwargs)

    def from_db_value(self, value: Path, expression, connection):
        if value is None:
            return value
        return parse_path(value)

    def to_python(self, values: Path):
        if isinstance(values, Path):
            return values

        if values is None:
            return values

        return parse_path(values)

    def __repr__(self):
        return f"Path({self.points.__repr__()})"

    def get_prep_value(self, values: Path):
        if values is None:
            return values

        if values:
            values = tuple(values.points)

        flat_coordinates = [
            str(item) for point in values for item in [point.x, point.y]]

        return ','.join(flat_coordinates)

    @require_postgres
    def db_type(self, connection):
        return 'path'


# =============================
# polygon


def parse_polygon(points):
    # polygons look like  ( ( x1 , y1 ) , ... , ( xn , yn ) )

    beginning = '('
    end = ')'
    points = points[len(beginning):-len(end)]

    coordinates = ''.join(
        [character for character in points if character not in ['(', ')']]).split(',')
    assert len(points) % 2 == 0

    doubles = []
    for coordinate_index in range(0, len(coordinates), 2):
        doubles.append(coordinates[coordinate_index:coordinate_index + 2])

    return Polygon([Point(int(double[0]), int(double[1])) for double in doubles])


class Polygon:
    def __init__(self, points):
        if len(points) < 3:
            raise ValueError("A Polygon needs at minimum 3 points")
        if points[0] != points[-1]:
            raise ValueError(
                "The first and last point of a polygon must be identical")
        self.points = points

    def __getitem__(self, index):
        if index not in range(len(self.points)):
            raise ValueError(
                f"Trying to get index {index} of a polygon that's only {len(self.points)} long is not allowed.")
        result = self.points[index]
        return result

    def __repr__(self):
        return f"Polygon({self.points.__repr__()})"

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        try:
            result = self[self.n]
            self.n += 1
            return result
        except ValueError:
            raise StopIteration

    def __len__(self):
        return len(self.points)


class PolygonField(models.Field):
    """
    Field to store a polygon (a list of at least three points, where the last is the same as the first). Looks like `( ( x1 , y1 ) , ... , ( xn , yn ) )` internally
    """

    def __init__(self, *args, **kwargs):
        # Input parameters are lists of cards ('Ah', '9s', etc.)
        super().__init__(*args, **kwargs)

    def from_db_value(self, value: Polygon, expression, connection):
        if value is None:
            return value
        return parse_polygon(value)

    def to_python(self, values: Polygon):
        if isinstance(values, Polygon):
            return values

        if values is None:
            return values

        return parse_polygon(values)

    def get_prep_value(self, values: Polygon):
        if values is None:
            return values

        if values:
            values = tuple(values.points)

        flat_coordinates = [
            str(item) for point in values for item in [point.x, point.y]]

        return ','.join(flat_coordinates)

    @require_postgres
    def db_type(self, connection):
        return 'polygon'

# =============================
# box


def parse_box(points):
    # boxes look like  ( x1 , y1 ) , ( x2 , y2 )

    coordinates = [int(i) for i in ''.join(
        [character for character in points if character not in ['(', ')']]).split(',')]
    assert len(points) == 4

    return Box(Point(coordinates[0], coordinates[1]), Point(coordinates[2], coordinates[3]))


class Box:
    def __init__(self, upper_right, lower_left):
        self.upper_right = upper_right
        self.lower_left = lower_left


class BoxField(models.Field):
    """
    Field to store a Box (2 points). Looks like `( x1 , y1 ) , ( x2 , y2 )` internally
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value: Box, expression, connection):
        if value is None:
            return value
        return parse_box(value)

    def to_python(self, values: Box):
        if isinstance(values, Box):
            return values

        if values is None:
            return values

        return parse_polygon(values)

    def __repr__(self):
        return f"BoxField({self.upper_right.__repr__()}, {self.lower_left.__repr__()})"

    def get_prep_value(self, values: Box):
        if values is None:
            return None

        return f'{values.upper_right.x}, {values.upper_right.y}, {values.lower_left.x}, {values.lower_left.y}'

    @require_postgres
    def db_type(self, connection):
        return 'box'

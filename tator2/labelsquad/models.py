from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from enum import Enum

from .django_postgres_geometry.fields import *
from tator2.users.models import User

# Create your models here.


class ClassTypeChoices(Enum):
    Polygon = 'Polygon'
    WholeImage = 'Whole image'


class ObjectClass(models.Model):
    class_type = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.value) for tag in ClassTypeChoices],
        default=ClassTypeChoices.Polygon,
    )

    name = models.CharField("Name", max_length=200)
    description = models.TextField("Description")

    def __str__(self):
        return self.name


class ImageCollection(models.Model):
    created_by = models.ForeignKey(User, related_name="created_collections",
                                   on_delete=models.CASCADE)
    can_edit = models.ManyToManyField(User)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField('Date created')

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(blank=True, null=True)

    uploaded_by = models.ForeignKey(User,
                                    on_delete=models.CASCADE)
    collection = models.ForeignKey(ImageCollection,
                                   on_delete=models.CASCADE)


class Annotation(models.Model):
    added_by = models.ForeignKey(User, null=True,
                                 on_delete=models.SET_NULL)

    classes = models.ManyToManyField(ObjectClass)
    #point = PointField(null=True)
    box = BoxField(null=True)
    path = PathField(null=True)
    polygon = PolygonField(null=True)

    image = models.ForeignKey(Image, null=True,
                              on_delete=models.SET_NULL)


class Project(models.Model):
    created_by = models.ForeignKey(User, related_name="created_projects",
                                   on_delete=models.CASCADE)
    can_edit = models.ManyToManyField(User)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    collections = models.ManyToManyField(ImageCollection, blank=True)
    classes = models.ManyToManyField(ObjectClass, blank=True)
    creation_date = models.DateTimeField('Date created')

    def __str__(self):
        return self.name

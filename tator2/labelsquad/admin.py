from django.contrib import admin

# Register your models here.
from .django_postgres_geometry.fields import *
from .models import *

admin.site.register(ObjectClass)
admin.site.register(ImageCollection)
admin.site.register(Image)
admin.site.register(Annotation)
admin.site.register(Project)

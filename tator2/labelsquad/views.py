from django.shortcuts import render

from .models import *


def index(request):
    image_collection_list = ImageCollection.objects.order_by(
        '-creation_date')
    project_list = Project.objects.order_by(
        '-creation_date')

    context = {'image_collection_list': image_collection_list,
               'project_list': project_list}

    return render(request, 'labelsquad/homepage.ejs', context)

from django.shortcuts import render
import json
from .models import *


def index(request):
    image_collection_list = ImageCollection.objects.order_by(
        '-creation_date')
    project_list = Project.objects.order_by(
        '-creation_date')

    props = {"a": ["1", "@", "3"]}

    context = {'image_collection_list': image_collection_list,
               'project_list': project_list,
               "props": json.dumps(props)}

    return render(request, 'labelsquad/reacttest.html', context)

from django.shortcuts import render
import json
from .models import *


def index(request):
    image_collection_list = ImageCollection.objects.order_by(
        '-creation_date')
    project_list = Project.objects.order_by(
        '-creation_date')

    props = {"collections": [{"owner": collec.created_by.username,
                              "name": collec.name,
                              "description": collec.description,
                              "id": collec.id,
                              "numImages": len(collec.image_set.all())} for collec in image_collection_list],

             "projects": [{"owner": project.created_by.username,
                           "name": project.name,
                           "description": project.description,
                           "id": project.id,
                           "numImages": len(project.collections.all())} for project in project_list]}

    context = {'image_collection_list': image_collection_list,
               'project_list': project_list,
               "props": json.dumps(props)}

    return render(request, 'labelsquad/reacttest.html', context)

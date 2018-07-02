from django.shortcuts import render
import json
from .models import *
from react.render import render_component


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

    context = {"props": json.dumps(props)}

    # rendered = render_component(
    #    'C:/Users/hyper/Documents/GitHub/annotator-tots/tator2/labelsquad/static/bundle.js', context)

    # print(rendered)

    return render(request, 'labelsquad/reacttest.html', context)

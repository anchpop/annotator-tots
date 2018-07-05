from django.shortcuts import render
import json
from .models import *
from react.render import render_component


def get_relative_url(absolute_uri):
    from six.moves.urllib.parse import urlparse
    return urlparse(absolute_uri).path


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
                           "numImages": len(project.collections.all())} for project in project_list],
             "on_server": True,
             "url":  get_relative_url(request.build_absolute_uri())}

    rendered = render_component(
        'C:/Users/hyper/Documents/GitHub/annotator-tots/tator2/labelsquad/src/root.jsx', props)

    props["on_server"] = False

    context = {"props": json.dumps(
        props), "rendered_html": rendered.markup, "rendered_css": rendered.css}

    return render(request, 'labelsquad/reacttest.html', context)

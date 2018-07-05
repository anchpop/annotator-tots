from django.shortcuts import render
import json
from .models import *
from react.render import render_component
from django.views import View
from collections import namedtuple
from pathlib import Path
import jsonpickle
import os


def get_relative_url(absolute_uri):
    from six.moves.urllib.parse import urlparse
    return urlparse(absolute_uri).path


RenderInfo = namedtuple(
    'RenderInfo', ['path_to_template', 'context', 'path_to_root_component'], verbose=True)


class ReactView(View):
    # JsonPickle will successfully encode to JSON what might be difficult otherwise, but can have large outputs which can slow down page load times. I don't reccomend it.
    USE_JSONPICKLE = False
    DEFAULT_ROOT_COMPONENT_PATH = './src/root.jsx'

    def get(self, request, *args, **kwargs):
        """Called when page is loaded"""
        render_info = self.getRenderInfo(request, *args, **kwargs)
        path_to_root_component = render_info.path_to_root_component if render_info.path_to_root_component is not None else self.DEFAULT_ROOT_COMPONENT_PATH
        path_to_root_component = Path(os.path.dirname(os.path.realpath(__file__)),
                                      path_to_root_component).resolve(strict=True)
        # Pass the URL as a prop
        render_info.context['props']['loaded_at_url'] = get_relative_url(
            request.build_absolute_uri())

        # Render the component on the server, typically for SEO reasons. If `REACT.render` is set to false in settings.py this will do nothing.
        # Set the `on_server` property to True, so you can render slightly differently on the client and server (useful for react-router)
        render_info.context['props']['on_server'] = True
        server_side_render = render_component(
            str(Path(path_to_root_component).resolve(strict=True)), render_info.context['props'])
        render_info.context['rendered_html'] = server_side_render.markup
        render_info.context['rendered_css'] = server_side_render.css
        print("markup: ", server_side_render.markup)

        # Set the `on_server` property to False, because we'll be sending this to the client
        render_info.context['props']['on_server'] = False
        # Convert props to json
        if self.USE_JSONPICKLE:
            render_info.context['props'] = jsonpickle.encode(
                render_info.context['props'], unpicklable=False)
        else:
            render_info.context['props'] = json.dumps(
                render_info.context['props'])

        return render(request, render_info.path_to_template, render_info.context)

    def getRenderInfo(self, request, *args, **kwargs) -> RenderInfo:
        """Abstract base class.
        Should return a namedtuple in the form of self.RenderInfo(path_to_template, context, path_to_root_component).
        If path_to_root_component is None, it will be assumed to be `src/root.jsx`.
        Whatever is at your path_to_root_component will be rendered on the server and passed to your template as `{{ rendered_html }}` and possibly `{{ rendered_css }}`. It will be passed `context.props` as its props. In addition, `props.on_server` will be True on the server but not on the client. A prop with the relative url the page was loaded on is also included at `props.loaded_at_url`."""
        raise NotImplementedError(
            "You need to subclass ReactView and override `getPage`.")


class Index(ReactView):
    def getRenderInfo(self, request, *args, **kwargs):
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
                 }
        # "on_server": True,}

        context = {"props":
                   props}  # , "rendered_html": rendered.markup, "rendered_css": rendered.css}

        return RenderInfo('labelsquad/reacttest.html', context, None)

        # rendered = render_component(
        #    'C:/Users/hyper/Documents/GitHub/annotator-tots/tator2/labelsquad/src/root.jsx', props)

        # props["on_server"] = False

        # return render(request, 'labelsquad/reacttest.html', context)

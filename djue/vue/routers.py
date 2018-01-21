#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from typing import Union

from django.conf import settings
from django.urls import RegexURLPattern, RegexURLResolver

from djue.factories import ViewFactory
from djue.management.commands._actions import generate_component
from djue.utils import render_to_js_string, flatten, replace
from djue.vue.core import ImportHelperMixin


class Route(ImportHelperMixin):
    lookup_name: str
    url: str = ''
    view = None
    children: [] = []
    file_ext = '.js'
    dir: str = ''

    # (?P<content_type_id>\d+)/(?P<object_id>.+)
    var_regex = '(\(\?P\<(\w+)\>[^)]*\))'

    def __init__(self, url: Union[RegexURLPattern, RegexURLResolver], app=''):
        self.url = self.extract_vue_route(url.regex.pattern)

        if isinstance(url, RegexURLResolver):
            app = app or url.app_name or url.urlconf_module.app_name or \
                  self.app
            self.lookup_name = url.namespace or app
            children = [Route(route, app) for route in url.url_patterns]

            # todo make this more elegant when not sick
            children = {child.lookup_name: child for child in children}
            self.children = children.values()

        elif isinstance(url, RegexURLPattern):
            app = app or url.lookup_str.split('.')[0]
            self.lookup_name = url.name or ''
            self.view = ViewFactory.create_from_callback(url.callback)
        else:
            raise Exception("Unknown object")

        super().__init__(app, 'routes')

    def render(self) -> str:
        imports = self.get_nested_import_paths()

        context = {'imports': imports, 'route': self}
        template = 'djue/routers.js'

        return render_to_js_string(template, context)

    def get_all_components(self) -> []:
        children = [x.get_all_components() for x in self.children]

        components = []
        for child in self.children:
            components += child.get_all_components()

        if self.view is not None:
            children.append(self.view)

        return children

    def get_nested_import_paths(self):
        imports = set()

        for view in flatten(self.get_all_components()):
            path = view.get_full_import_string('../../') if self.app != view.app \
                else view.create_import_string(view.module_path)
            imports.add(path)

        return imports

    def extract_vue_route(self, pattern: str):
        route = re.sub(self.var_regex, replace, pattern)
        format = getattr(settings, 'DJUE_FORMAT', 'json')

        return route.replace('^', '').replace('$', '').replace(':format',
                                                               format)


class Router:
    routes: {} = {}

    def __init__(self, resolver: RegexURLResolver):
        app = getattr(resolver.urlconf_module, 'app_name', None)

        for url in resolver.url_patterns:
            route = Route(url, app)

            self.routes[route.lookup_name] = route

    def create_routes(self):
        root = getattr(settings, 'DJUE_OUTPUT_DIR', os.getcwd())
        path = os.path.join(root, 'src')
        os.makedirs(path, exist_ok=True)

        for name, route in self.routes.items():
            generate_component(route, path)

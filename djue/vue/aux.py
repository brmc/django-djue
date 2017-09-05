#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from typing import Union

from django.conf import settings
from django.urls import RegexURLPattern, RegexURLResolver

from djue.factories import ViewFactory
from djue.utils import replace, render_to_js_string, flatten


class Route:
    app_name: str = 'default'
    name: str = ''
    path: str = ''
    view = None
    children: [] = []
    # (?P<content_type_id>\d+)/(?P<object_id>.+)
    var_regex = '(\(\?P\<(\w+)\>[^\/]*\))'

    def __init__(self, url: Union[RegexURLPattern, RegexURLResolver],
                 app=''):
        self.path = self.extract_vue_route(url.regex.pattern)

        if isinstance(url, RegexURLResolver):
            app = app or url.app_name or self.app_name
            self.app_name = app
            self.name = url.namespace or app
            self.children = [Route(route, app) for route in url.url_patterns]
        elif isinstance(url, RegexURLPattern):
            self.app_name = app or url.lookup_str.split('.')[0]
            self.name = url.name or ''

            self.view = ViewFactory.create_from_callback(url.callback)
        else:
            raise Exception("Unknown object")

    def get_all_components(self):
        children = [x.get_all_components() for x in self.children]

        components = []
        for child in self.children:
            components += child.get_all_components()

        if self.view is not None:
            children.append(self.view)

        return children

    def get_nested_import_paths(self, root='..'):
        imports = []
        for view in flatten(self.get_all_components()):
            imports.append(view.relative_module_import_string)

        return imports

    def extract_vue_route(self, pattern: str):
        route = re.sub(self.var_regex, replace, pattern)

        return route.replace('^', '').replace('$', '')


class Router:
    routes: {} = {}

    def __init__(self, resolver: RegexURLResolver):
        for url in resolver.url_patterns:
            route = Route(url)

            self.routes[route.name] = route

    def create_routes(self):
        root = getattr(settings, 'PROJECT_ROOT', os.getcwd())
        path = os.path.join(root, 'src/routers')
        os.makedirs(path, exist_ok=True)

        for name, route in self.routes.items():
            file_path = os.path.join(path, route.app_name + '.js')
            imports = route.get_nested_import_paths()

            context = {'imports': imports, 'route': route}
            template = 'djue/routers.js'

            output = render_to_js_string(template, context)

            with open(file_path, 'w+') as file:
                file.write(output)


class StoreModule:
    pass


class Store:
    pass

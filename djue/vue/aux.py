#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from typing import Union

from django.conf import settings
from django.urls import RegexURLPattern, RegexURLResolver

from djue.factories import ViewFactory
from djue.management.commands._actions import generate_component
from djue.utils import replace, render_to_js_string, flatten
from djue.vue.core import ImportHelperMixin


class Route(ImportHelperMixin):
    lookup_name: str
    url: str = ''
    view = None
    children: [] = []
    file_ext = '.js'
    dir: str = ''

    # (?P<content_type_id>\d+)/(?P<object_id>.+)
    var_regex = '(\(\?P\<(\w+)\>[^\/]*\))'

    def __init__(self, url: Union[RegexURLPattern, RegexURLResolver], app=''):
        self.url = self.extract_vue_route(url.regex.pattern)

        if isinstance(url, RegexURLResolver):
            app = app or url.app_name or self.app
            self.lookup_name = url.namespace or app
            self.children = [Route(route, app) for route in url.url_patterns]
        elif isinstance(url, RegexURLPattern):
            app = app or url.lookup_str.split('.')[0]
            self.lookup_name = url.name or ''
            self.view = ViewFactory.create_from_callback(url.callback)
        else:
            raise Exception("Unknown object")

        super().__init__(app, 'routes')

    def render(self):
        imports = self.get_nested_import_paths()

        context = {'imports': imports, 'route': self}
        template = 'djue/routers.js'

        return render_to_js_string(template, context)

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
            imports.append(view.create_import_string(view.module_path))

        return imports

    def extract_vue_route(self, pattern: str):
        route = re.sub(self.var_regex, replace, pattern)

        return route.replace('^', '').replace('$', '')


class Router:
    routes: {} = {}

    def __init__(self, resolver: RegexURLResolver):
        for url in resolver.url_patterns:
            route = Route(url)

            self.routes[route.lookup_name] = route

    def create_routes(self):
        root = getattr(settings, 'PROJECT_ROOT', os.getcwd())
        path = os.path.join(root, 'src')
        os.makedirs(path, exist_ok=True)

        for name, route in self.routes.items():
            generate_component(route, path)


class StoreModule:
    pass


class Store(ImportHelperMixin):
    file_ext: str = '.js'
    name: str = 'store'
    dir: str = ''

    def __init__(self, app, fields):
        self.fields = fields

        super().__init__(app, self.name)

    def render(self):
        return render_to_js_string('djue/store-module.js',
                                   {'fields': self.fields})

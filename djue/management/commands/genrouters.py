#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import re
from typing import Union, List

import jsbeautifier
from django.conf import settings
from django.core.management import BaseCommand
from django.forms import ModelForm
from django.template.loader import render_to_string
from django.urls import RegexURLPattern, RegexURLResolver
from editorconfig import PathError


def flatten(lst):
    if isinstance(lst, list):
        if lst == []:
            return lst
        head, tail = lst[0], lst[1:]
        return flatten(head) + flatten(tail)
    else:
        return [lst]


def convert_to_pascalcase(string: str):
    return "".join([word.capitalize() for word in string.split('_')])


def convert_to_camelcase(string: str):
    string = convert_to_pascalcase(string)

    return string[0].lower() + string[1:]


def my_replace(match):
    match = match.group()
    return match + str(match.index('e'))


def replace(match):
    return ':' + match.groups()[-1]


class InvalidUrlObject(Exception):
    pass


class Route:
    app_name: str = 'default'
    name: str = ''
    path: str = ''
    component: str = None
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

            callback = url.callback.__name__

            if not hasattr(url.callback, 'view_class'):
                callback = convert_to_camelcase(callback)

            self.component = callback
        else:
            raise Exception("Unknown object")

            # view = url.callback.view_class()
            # view.object = None
            # view.object_list = None
            # templates = view.get_template_names()
            #
            # from django.template.loader import select_template
            #
            # try:
            #     template = select_template(templates)
            # except TemplateDoesNotExist as e:
            #     msg = """ No template was found when trying to create a
            # view model
            #     for
            #
            #     """

    def get_all_components(self):
        children = [x.get_all_components() for x in self.children]

        components = []
        for child in self.children:
            components += child.get_all_components()

        if self.component is not None:
            children.append(
                {'app': self.app_name, 'component': self.component})

        return children

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
            imports = View.create_import_paths(route.get_all_components())

            context = {'imports': imports, 'route': route}
            template = 'djue/routers.js'

            output = render_to_js_string(template, context)

            with open(file_path, 'w+') as file:
                file.write(output)


def render_to_js_string(template, context):
    output = render_to_string(template, context)
    options = jsbeautifier.default_options()

    opts_file = getattr(settings, 'EDITOR_CONFIG', '.editorconfig')

    try:
        jsbeautifier.set_file_editorconfig_opts(opts_file, options)
    except PathError:
        print("No editor config found at: {opts_file}\n"
              "Using defaults.")

    return jsbeautifier.beautify(output, opts=options)


class Component:
    pass


class View:
    @staticmethod
    def create_import_paths(components, root='..'):
        import_str = "import {} from '{}.js'"
        imports = []
        for component in flatten(components):
            app = component.get('app')
            component = component.get('component')
            directory = os.path.join(root,
                                     'views',
                                     app,
                                     component)
            imports.append(import_str.format(component, directory))

        return imports

    form: ModelForm

    def __init__(self, form: ModelForm, *args, **kwargs):
        self.form = form


class StoreModule:
    pass


class Store:
    pass


class App:
    router: Router
    store: Store
    views: List[View]
    components: List[Component]


class Command(BaseCommand):
    help = 'fuyck you'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('modules', nargs='+', type=str)
        parser.add_argument('--drf')

    def handle(self, *args, **options):
        modules = options.get('modules', )

        for module in options['modules']:
            from django.urls.resolvers import get_resolver

            module = get_resolver(module)

            router = Router(module)
            router.create_routes()
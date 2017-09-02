#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from typing import List, Type

import sys
from django.conf import settings
from django.forms import ModelForm, forms
from django.template import loader
from django.template.loader import render_to_string
from django.apps import apps
from django.urls import RegexURLPattern, RegexURLResolver, get_resolver
from django.views import View as DjangoView
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import BaseListView

from djue.management.commands._actions import ModuleCommand
from djue.utils import flatten, render_to_js_string


def as_vue(self):
    for name, field in self.fields.items():
        template: str = field.widget.template_name
        field.widget.template_name = template.replace('django/forms', 'djue')

    return self.as_p()


def get_app_name(obj):
    try:
        return apps.get_containing_app_config(obj.__module__).name
    except AttributeError:
        sys.stdout.write(
            "Object is not part of an app. About to do stupid shit")
        return 'default'
        return os.path.join(*obj.__module__.split('.'))


class ImportHelperMixin:
    root: str = 'modules'
    name: str = ''
    obj: forms.Form
    file_ext: str = '.vue'

    @property
    def path(self):
        app = get_app_name(self.obj)
        self._path = os.path.join(self.root, app, self.module_path)

        return self._path

    @property
    def module_path(self):
        file = self.name + self.file_ext
        return os.path.join(self.dir, file)

    def get_import_string(self, relative_to=''):
        path = self.get_relative_path(relative_to)

        return f"import {{{self.name}}} from '{path}'"

    def get_relative_path(self, to):
        return os.path.join(to, self.path)

    def get_relative_module_path(self, to):
        return os.path.join(to, self.module_path)


class Component(ImportHelperMixin):
    module: str
    name: str
    dir: str = 'components'
    obj: object

    def __init__(self, obj):
        self.obj = obj
        super().__init__()

    @staticmethod
    def create_import_paths(components, root='..'):
        import_str = "import {} from '{}.vue'"

        imports = []
        for component in components:
            name = component.name
            directory = os.path.join(root, 'components', component.app, name)

            imports.append(import_str.format(name, directory))

        return imports


class FormComponent(Component):
    obj: Type[forms.Form]

    def __init__(self, form: Type[forms.Form], *args, **kwargs):
        form.as_vue = as_vue
        self.name = form.__name__
        self.model = form._meta.model.__name__

        super().__init__(form)

    def render(self):
        form = self.obj()

        html = render_to_string('djue/component.html',
                                {'form': form})

        js = render_to_js_string('djue/component.js',
                                 {'form': form, 'model': self.model})

        return render_to_string('djue/component.vue',
                                {'html': html, 'js': js})


class View:
    form: ModelForm

    @staticmethod
    def create_import_paths(views, root='..'):
        import_str = "import {} from '{}.vue'"
        imports = []
        for view in flatten(views):
            app = view.get('module')
            name = view.get('name')
            directory = os.path.join(root, 'views', app, name)
            imports.append(import_str.format(view, directory))

        return imports

    def __init__(self, view: DjangoView, *args, **kwargs):
        loader.get_template(view)

        if hasattr(view, 'template_name'):
            self.template = loader.get_template(view.template_name).source


class ComponentFactory:
    @staticmethod
    def create_component(view):
        type_of = type(view)
        msg = "not implemented for {}: {}\nskipping..."
        if not hasattr(view, 'view_class'):
            sys.stdout.write(msg.format('callable views', view.__name__))
            return

        cls = view.view_class()
        if isinstance(cls, ModelFormMixin):
            form_class = cls.get_form_class()
            return FormComponent(form_class)
        elif isinstance(cls, (BaseListView, BaseDetailView)):
            sys.stdout.write('detail views not implemented: \n')
            sys.stdout.write(msg.format("detail views", view.__name__))


from django.views.generic import ListView, DetailView, CreateView


def generate_components(patterns, path):
    print(1)
    for url in patterns:
        print(url)
        if isinstance(url, RegexURLResolver):
            sys.stdout.write(
                'URL Resolver found! Stepping down the rabbit hole...')
            generate_components(url.url_patterns)

        component = ComponentFactory.create_component(url.callback)

        if not component:
            sys.stdout.write('No Component was generated for: ')
            sys.stdout.write(str(url))
            continue

        file_path = os.path.join(path, component.path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w+') as file:
            sys.stdout.write('writing to ' + file_path)
            file.write(component.render())


class Command(ModuleCommand):
    def handle(self, *args, **options):
        modules = options.get('modules', [])
        root = getattr(settings, 'PROJECT_ROOT', os.getcwd())

        path = os.path.join(root, 'src')
        os.makedirs(path, exist_ok=True)

        for module in modules:
            sys.stdout.write(f'Generating components for {module}\n')
            module = get_resolver(module)
            generate_components(module.url_patterns, path)

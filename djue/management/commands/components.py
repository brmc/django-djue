#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from typing import Type

from django.conf import settings
from django.forms import ModelForm, forms
from django.template import loader
from django.template.loader import render_to_string
from django.urls import get_resolver
from django.views import View as DjangoView
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import BaseListView

from djue.management.commands._actions import ModuleCommand, \
    generate_components
from djue.utils import flatten, render_to_js_string, render_to_html_string, \
    as_vue, get_app_name


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

        html = render_to_html_string('djue/component.html',
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
    def create_from_callback(callback):
        msg = "not implemented for {}: {}\nskipping..."
        if not hasattr(callback, 'view_class'):
            sys.stdout.write(msg.format('callable views', callback.__name__))
            return

        view = callback.view_class()

        if isinstance(view, ModelFormMixin):
            form_class = view.get_form_class()

            return ComponentFactory.create_from_form(form_class)
        elif isinstance(view, (BaseListView, BaseDetailView)):
            ComponentFactory.create_from_template(callback, msg)

    @staticmethod
    def create_from_template(callback, msg):
        sys.stdout.write('detail views not implemented: \n')
        sys.stdout.write(msg.format("detail views", callback.__name__))

    @staticmethod
    def create_from_form(form_class):
        return FormComponent(form_class)


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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.forms import ModelForm
from django.template.loader import render_to_string

from djue.management.commands._actions import ModuleCommand
from djue.utils import flatten


def as_vue(self):
    for name, field in self.fields.items():
        template: str = field.widget.template_name
        field.widget.template_name = template.replace('django/forms', 'djue')

    return self.as_p()


class Component:
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


class Command(ModuleCommand):
    def handle(self, *args, **options):
        modules = options.get('modules', [])
        root = getattr(settings, 'PROJECT_ROOT', os.getcwd())

        path = os.path.join(root, 'src/routers')
        os.makedirs(path, exist_ok=True)
        for module in modules:
            from django.urls.resolvers import get_resolver
            file_path = os.path.join(path, 'x' + '.vue')

            module = get_resolver(module).url_patterns[0]
            view_class = module.callback.view_class

            form_class = view_class().get_form_class()
            form_class.as_vue = as_vue
            output = render_to_string('djue/component.vue',
                                      {'form': form_class()})

            with open(file_path, 'w+') as file:
                file.write(output)

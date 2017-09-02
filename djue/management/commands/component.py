#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import sys
from importlib import import_module

from django.conf import settings
from django.urls import get_resolver
from django.utils.module_loading import import_string

from djue.management.commands._actions import ModuleCommand
from djue.management.commands.components import generate_components, \
    generate_component, ComponentFactory


class Command(ModuleCommand):
    def handle(self, *args, **options):
        modules = options.get('modules', [])
        root = getattr(settings, 'PROJECT_ROOT', os.getcwd())

        path = os.path.join(root, 'src')
        os.makedirs(path, exist_ok=True)

        for module in modules:
            sys.stdout.write(f'Generating component: {module}\n')
            form = import_string(module)

            component = ComponentFactory.create_from_form(form)
            generate_component(component, path)

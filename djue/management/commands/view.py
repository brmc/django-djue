#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from django.conf import settings
from django.utils.module_loading import import_string

from djue.management.commands._actions import ModuleCommand, generate_component
from djue.factories import ComponentFactory
from djue.utils import log
from djue.vue.views import ModelView


class Command(ModuleCommand):
    def handle(self, *args, **options):
        modules = options.get('modules', [])
        root = getattr(settings, 'PROJECT_ROOT', os.getcwd())

        path = os.path.join(root, 'src')
        os.makedirs(path, exist_ok=True)

        for module in modules:
            log(f'Generating view: {module}\n')
            form = import_string(module)

            component = ModelView(form)
            generate_component(component, path)

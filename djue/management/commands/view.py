#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.utils.module_loading import import_string

from djue.factories import ViewFactory
from djue.management.commands._actions import ModuleCommand, generate_component
from djue.utils import log


class Command(ModuleCommand):
    def handle(self, *args, **options):
        modules = options.get('modules', [])
        root = getattr(settings, 'DJUE_OUTPUT_DIR', os.getcwd())

        path = os.path.join(root, 'src')
        os.makedirs(path, exist_ok=True)

        for module in modules:
            log(f'Generating view: {module}\n')
            view = import_string(module)

            component = ViewFactory.create_from_view(view)
            generate_component(component, path)

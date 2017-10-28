#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.utils.module_loading import import_string

from djue.factories import StoreFactory
from djue.management.commands._actions import ModuleCommand, generate_component
from djue.utils import log


class Command(ModuleCommand):
    def handle(self, *args, **options):
        modules = options.get('modules', [])
        root = getattr(settings, 'DJUE_OUTPUT_DIR', os.getcwd())

        path = os.path.join(root, 'src')
        os.makedirs(path, exist_ok=True)

        for module in modules:
            log(f'Generating store module: {module}\n')
            form = import_string(module)

            if hasattr(form, '_meta'):
                component = StoreFactory.create_from_form(form)
            elif hasattr(form, 'Meta'):
                component = StoreFactory.create_from_serializer(form)
            else:
                log(f'Could not create vue store from {module}')
                continue

            generate_component(component, path)

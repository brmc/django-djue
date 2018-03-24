#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.utils.module_loading import import_string

from djue.factories import StoreFactory
from djue.management.commands._actions import ModuleCommand, generate_component
from djue.utils import log, get_output_path


class Command(ModuleCommand):
    def handle(self, *args, **options):
        path = get_output_path()

        for module in options.get('modules', []):
            log(f'Generating store module: {module}\n')
            form = import_string(module)

            if hasattr(form, '_meta'):
                component = StoreFactory.from_form(form)
            elif hasattr(form, 'Meta'):
                component = StoreFactory.from_serializer(form)
            else:
                log(f'Could not create vue store from {module}')
                continue

            generate_component(component, path)

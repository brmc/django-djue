#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from django.utils.module_loading import import_string

from djue.factories import ViewFactory
from djue.management.commands._actions import ModuleCommand, generate_component
from djue.utils import log, get_output_path


class Command(ModuleCommand):
    def handle(self, *args, **options):
        path = get_output_path()

        for module in options.get('modules', []):
            log(f'Generating view: {module}\n')
            view = import_string(module)

            component = ViewFactory.from_view(view)
            generate_component(component, path)

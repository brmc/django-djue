#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.module_loading import import_string

from djue.management.commands._actions import ModuleCommand, generate_component
from djue.factories import ComponentFactory
from djue.utils import log, get_output_path


class Command(ModuleCommand):
    def handle(self, *args, **options):
        path = get_output_path()

        for module in options.get('modules', []):
            log(f'Generating component: {module}')
            form = import_string(module)

            component = ComponentFactory.create_from_form(form)
            generate_component(component, path)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from django.conf import settings
from django.urls import get_resolver

from djue.management.commands._actions import ModuleCommand, \
    generate_components


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

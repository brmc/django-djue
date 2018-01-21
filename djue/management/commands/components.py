#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from django.conf import settings
from django.urls import get_resolver

from djue.management.commands._actions import ModuleCommand, \
    generate_components
from djue.utils import log, get_output_path


class Command(ModuleCommand):
    def handle(self, *args, **options):
        path = get_output_path()

        for module in options.get('modules', []):
            log(f'Generating components for {module}')
            module = get_resolver(module)

            generate_components(module.url_patterns, path)

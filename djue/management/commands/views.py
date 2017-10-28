#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from django.conf import settings
from django.urls import get_resolver, RegexURLResolver

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
            log(f'Generating views for {module}')
            module = get_resolver(module)
            generate_views(module.url_patterns, path)


def generate_views(patterns, path):
    for url in patterns:
        log(f'url: {url.regex.pattern}')
        if isinstance(url, RegexURLResolver):
            log('URL Resolver found! Stepping down the rabbit hole...')

            generate_views(url.url_patterns, path)
            continue

        callback = url.callback

        if hasattr(callback, 'actions'):
            log('Generating views from DRF ViewSet...')
            component = ViewFactory.create_from_viewset(callback)
        else :
            component = ViewFactory.create_from_callback(callback)

        if not component:
            log(f'No Component was generated for: {str(url)}')
            continue

        generate_component(component, path)

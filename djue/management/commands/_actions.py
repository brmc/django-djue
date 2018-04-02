#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os

from django.core.management import BaseCommand
from django.urls import RegexURLResolver

from djue.factories import ComponentFactory
from djue.utils import log
from djue.vue.core import SingleFileComponent


class ModuleCommand(BaseCommand):
    help = 'fuyck you'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('modules', nargs='+', type=str)
        parser.add_argument('--drf')


def generate_components(patterns, path):
    for url in patterns:
        log(f'url: {url.regex.pattern}')
        if isinstance(url, RegexURLResolver):
            log('URL Resolver found! Stepping down the rabbit hole...')
            generate_components(url.url_patterns, path)
            continue

        callback = url.callback
        if hasattr(callback, 'actions'):
            for method, action in callback.actions.items():
                comp, form = ComponentFactory.from_junk(callback, method,
                                                        action)
                comp.add_context({'route': url.name})
                comp.write()
                form and form.write()

            continue

        component, form = ComponentFactory.from_callback(callback)

        if not component:
            log(f'No Component was generated for: {str(url)}')
            continue
        component.add_context({'route': url.name})
        component.write()

        form and form.write()


def generate_component(component: SingleFileComponent, path: str):
    file_path = os.path.join(path, component.path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w+') as file:
        log('writing to ' + file_path)
        file.write(component.render())

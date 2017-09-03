#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import sys

from django.core.management import BaseCommand
from django.urls import RegexURLResolver

from djue.factories import ComponentFactory


class ModuleCommand(BaseCommand):
    help = 'fuyck you'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('modules', nargs='+', type=str)
        parser.add_argument('--drf')


def generate_components(patterns, path):
    for url in patterns:
        if isinstance(url, RegexURLResolver):
            sys.stdout.write(
                'URL Resolver found! Stepping down the rabbit hole...')
            generate_components(url.url_patterns, path)

        component = ComponentFactory.create_from_callback(url.callback)

        if not component:
            sys.stdout.write('No Component was generated for: ')
            sys.stdout.write(str(url))
            continue


def generate_component(component, path):
    file_path = os.path.join(path, component.path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w+') as file:
        sys.stdout.write('writing to ' + file_path)
        file.write(component.render())
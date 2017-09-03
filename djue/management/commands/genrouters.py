#!/usr/bin/env python
# -*- coding: utf-8 -*-

from djue.management.commands._actions import ModuleCommand
from djue.vue.aux import Router


class InvalidUrlObject(Exception):
    pass


class Command(ModuleCommand):
    help = 'fuyck you'

    def handle(self, *args, **options):
        modules = options.get('modules', [])

        for module in modules:
            from django.urls.resolvers import get_resolver

            module = get_resolver(module)

            router = Router(module)
            router.create_routes()

            router.create()
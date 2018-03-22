#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._actions import ModuleCommand


class Command(ModuleCommand):
    def handle(self, *args, **options):
        stuff = {
            'components': 'components',
            'store': 'store',
            'views': 'views',
            'util': 'util.js',
            'main': 'main.js',
        }

        print(1)
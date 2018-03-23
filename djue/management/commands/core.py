#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import sys

from djue.utils import get_output_path, log
from djue.vue.components import StaticComponent
from ._actions import ModuleCommand, generate_component

class CoreComponent(StaticComponent):
    root = ''


class Command(ModuleCommand):
    def handle(self, *args, **options):
        stuff = {
            'components': 'components',
            'store': 'store',
            'views': 'views',
            'util': 'util.js',
            'main': 'main.js',
        }

        base = 'djue/core/'

        for option in options['modules']:
            module = stuff.get(option)

            if module is None:
                log(f'"{option}" is an invalid core module')
                log(f'Please select from: {stuff.keys()}')
                continue
            path = base + module
            if os.path.isdir(path):
                for dirname, dirs, files in os.walk(path):
                    print(dirname)


            return
        c = CoreComponent('djue/core/components/Serializer.vue', app='', name='')
        print(c.root)
        #generate_component(c, get_output_path())
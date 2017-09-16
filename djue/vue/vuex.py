#!/usr/bin/env python
# -*- coding: utf-8 -*-

from djue.utils import render_to_js_string
from djue.vue.core import ImportHelperMixin


class StoreModule:
    pass


class Store(ImportHelperMixin):
    file_ext: str = '.js'
    name: str = 'store'
    dir: str = ''

    def __init__(self, app, fields):
        self.fields = fields

        super().__init__(app, self.name)

    def render(self):
        return render_to_js_string('djue/store-module.js',
                                   {'fields': self.fields})

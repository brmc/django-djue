#!/usr/bin/env python
# -*- coding: utf-8 -*-

from djue.utils import render_to_js_string, flatten
from djue.vue.core import ImportHelperMixin


class StoreModule:
    pass


class Store(ImportHelperMixin):
    file_ext: str = '.js'
    dir: str = 'stores'

    def __init__(self, app, name, fields):
        self.fields = fields

        super().__init__(app, name)

    def render(self):
        validators = flatten([field.validator_names for field in self.fields])
        return render_to_js_string('djue/store-module.js',
                                   {'fields': self.fields,
                                    'validators': validators})

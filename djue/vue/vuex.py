#!/usr/bin/env python
# -*- coding: utf-8 -*-
from djue.vue.renderers import PlainJsMixin
from djue.vue.base import ModuleFile
from djue.utils import render_to_js_string, flatten
from djue.vue.core import ImportHelperMixin


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
                                    'name': self.name,
                                    'validators': validators})


class StoreModule(PlainJsMixin, ModuleFile):
    dir: str = 'stores'
    file_ext: str = '.js'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = 'djue/modules/store-module.js'


class ModuleStore(PlainJsMixin, ModuleFile):
    dir: str = 'store'
    file_ext: str = '.js'
    modules: []

    def __init__(self, app, modules):
        super().__init__(app, 'store')
        self.modules = modules
        self.template = 'djue/modules/module-store.js'

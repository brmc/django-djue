#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from django.template.loader import render_to_string

from djue.utils import get_app_name


class ImportHelperMixin:
    root: str = 'modules'
    name: str = ''
    obj: object
    file_ext: str = '.vue'
    dir: str = ''

    @property
    def path(self):
        app = get_app_name(self.obj)
        self._path = os.path.join(self.root, app, self.module_path)

        return self._path

    @property
    def module_path(self):
        file = self.name + self.file_ext
        return os.path.join(self.dir, file)

    def get_full_import_string(self, relative_to=''):
        path = self.get_relative_path(relative_to)

        return self.create_import_string(path)

    def create_import_string(self, path):
        return f"import {self.name} from '{path}'"

    def get_relative_path(self, to):
        return os.path.join(to, self.path)

    def get_relative_module_path(self, to='..'):
        return os.path.join(to, self.module_path)

    @property
    def relative_module_import_string(self):
        return self.create_import_string(self.get_relative_module_path())


class VueBase(ImportHelperMixin):
    module: str = ''
    name: str = ''
    dir: str = ''
    obj: object

    def __init__(self, obj):
        self.obj = obj
        super().__init__()

    def render_sfc(self, html, js):
        return render_to_string('djue/sfc.vue', {'html': html, 'js': js})

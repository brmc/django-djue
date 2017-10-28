#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from django.template.loader import render_to_string


class ImportHelperMixin:
    root: str = 'modules'
    file_ext: str = '.vue'
    name: str = ''
    dir: str = ''
    app: str

    def __init__(self, app, name, js=None, html=None):
        self.app = app
        self.name = name
        self.js = js
        self.html = html

        super().__init__()

    @property
    def path(self):
        self._path = os.path.join(self.root, self.app,
                                  self.module_path)

        return self._path

    @property
    def module_path(self):
        file = self.name + self.file_ext
        return os.path.join('.', self.dir, file)

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


class SingleFileComponent(ImportHelperMixin):
    def render_sfc(self, html, js):
        return render_to_string('djue/sfc.vue', {'html': html, 'js': js})

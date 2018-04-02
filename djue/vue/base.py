#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from abc import ABC, abstractmethod
from typing import Type

from djue.vue.renderers import PlainJsMixin, StaticFileMixin
from djue.vue.writers import SimpleWriter


class VueFile(ABC):
    root: str = ''
    writer_cls: Type[SimpleWriter] = SimpleWriter
    file_ext = ''

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.writer = self.writer_cls(self.path)

    @property
    @abstractmethod
    def path(self):
        pass

    @abstractmethod
    def render(self):
        pass

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

    def write(self):
        self.writer.write(self.render())


class CoreFile(VueFile):
    root = 'core'
    dir: str
    name: str
    file_ext: str

    def __init__(self, name, dir_=''):
        self.dir = dir_
        super().__init__(name)


class ModuleFile(VueFile):
    root = 'modules'
    app: str
    dir: str
    name: str
    file_ext: str

    def __init__(self, app: str, name: str):
        self.app = app
        super().__init__(name)

    @property
    def path(self):
        return os.path.join(self.root, self.app, self.module_path)


class StaticFile(StaticFileMixin, VueFile):
    @property
    def path(self):
        return os.path.join(self.output_path, self.name + self.file_ext)

    def __init__(self, template, output_path, file_ext=None, name=None):
        self.output_path = output_path
        alt_name, ext = template.split(os.sep)[-1].split('.')
        name = name or alt_name
        self.file_ext = file_ext or '.' + ext

        super().__init__(template, name)


class ModuleJs(PlainJsMixin, ModuleFile):
    file_ext: str = '.js'

    def __init__(self, app, name, dir_=''):
        self.dir = dir_
        super().__init__(app, name)

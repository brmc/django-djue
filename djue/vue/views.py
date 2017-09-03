#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from django.forms import ModelForm
from django.template import loader
from django.views import View as DjangoView

from djue.utils import flatten


class View:
    form: ModelForm

    @staticmethod
    def create_import_paths(views, root='..'):
        import_str = "import {} from '{}.vue'"
        imports = []
        for view in flatten(views):
            app = view.get('module')
            name = view.get('component')
            directory = os.path.join(root, 'views', app, name)
            imports.append(import_str.format(name, directory))

        return imports

    def __init__(self, view: DjangoView, *args, **kwargs):
        loader.get_template(view)

        if hasattr(view, 'template_name'):
            self.template = loader.get_template(view.template_name).source
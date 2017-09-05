#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from typing import Type

from django.forms import ModelForm
from django.template import loader
from django.views import View as DjangoView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from djue.utils import flatten, render_to_js_string
from djue.vue import FormComponent
from djue.vue.core import VueBase


class Vue(VueBase):
    dir = 'views'
    template: str = ''


class ModelView(Vue):
    obj: Type[SingleObjectMixin]

    def __init__(self, view: TemplateResponseMixin):
        self.name = view.__name__

        self.template = loader.select_template(
            view().get_template_names()).template

        if hasattr(view, 'form_class'):
            self.components = [FormComponent(view.form_class)]

        super().__init__(view)

    def render(self):
        html = self.template.source
        component = self.components[0].name
        html = f'<{component}></{component}>'

        js = render_to_js_string('djue/view.js',
                                 {'components': self.components})

        return self.render_sfc(html, js)


class Vue2(Vue):
    def __init__(self, app, template, components, obj):
        super().__init__(obj)


class MultiObjectView(Vue):
    obj: Type[MultipleObjectMixin]

    def __init__(self, view: Type[MultipleObjectMixin]):
        self.model = view.model.__name__
        super().__init__(view)


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

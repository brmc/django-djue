#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Type

from django.forms import forms
from django.template import Template

from djue.utils import as_vue, render_to_html_string, render_to_js_string, \
    convert_file_to_component_name
from djue.vue.core import VueBase


class Component(VueBase):
    dir: str = 'components'


class FormComponent(Component):
    obj: Type[forms.Form]

    def __init__(self, form: Type[forms.Form], *args, **kwargs):
        form.as_vue = as_vue
        self.name = form.__name__
        self.model = form._meta.model.__name__

        super().__init__(form)

    def render(self):
        form = self.obj()

        html = render_to_html_string('djue/component.html',
                                     {'form': form})

        js = render_to_js_string('djue/component.js',
                                 {'form': form, 'model': self.model})

        return self.render_sfc(html, js)


class TemplateComponent(Component):
    obj: Template
    def __init__(self, template: Template, app: str):
        self.name = convert_file_to_component_name(template.name) + 'Template'
        super().__init__(template, app)

    def render(self):
        html = self.obj.source
        js = ''

        return self.render_sfc(html, js)


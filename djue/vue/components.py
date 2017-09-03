#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Type

from django.forms import forms
from django.template.loader import render_to_string

from djue.utils import as_vue, render_to_html_string, render_to_js_string
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

        return render_to_string('djue/component.vue',
                                {'html': html, 'js': js})

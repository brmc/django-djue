#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Type

from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin

from djue.utils import render_to_js_string, convert_to_camelcase
from djue.vue.core import VueBase


class Vue(VueBase):
    dir = 'views'
    template: str = ''


class View(Vue):
    def __init__(self, components, *args, **kwargs):
        self.components = components

        super().__init__(*args, **kwargs)

    def render(self):
        component = self.components[0].name
        html = f'<{component}></{component}>'

        js = render_to_js_string('djue/view.js',
                                 {'components': self.components})

        return self.render_sfc(html, js)


class FunctionalView(Vue):
    def __init__(self, components, *args, **kwargs):
        self.components = components

        super().__init__(*args, **kwargs)

    def render(self):
        component = self.components[0].name
        html = f'<{component}></{component}>'

        js = render_to_js_string('djue/view.js',
                                 {'components': self.components})

        return self.render_sfc(html, js)

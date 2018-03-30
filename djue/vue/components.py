#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.template import Template
from django.template.loader import render_to_string

from djue.utils import render_to_html_string, render_to_js_string
from djue.vue.core import SingleFileComponent, CrudMixin


class Component(SingleFileComponent):
    root: str = 'modules'
    dir: str = 'components'


class CrudComponent(CrudMixin, Component):
    pass


class AnonComponent(CrudComponent):
    def render(self):
        html = ''
        js = render_to_js_string('djue/template_component.js', {})

        return self.render_sfc(html, js)


class ReadComponent(CrudComponent):
    def __init__(self, action: str, component=None, *args, **kwargs):
        self.action = action
        self.component = component
        self.template_name = f'djue/actions/{action}.html'
        super().__init__(*args, **kwargs)

    def render(self):
        html = render_to_html_string(self.template_name, {})
        js = render_to_js_string(f'djue/actions/{self.action}.js',
                                 {'self': self})

        return self.render_sfc(html, js)


class FormComponent(CrudComponent):
    def __init__(self, form, *args, **kwargs):
        self.form = form

        super().__init__(*args, **kwargs)

    def render(self):
        form = self.form

        html = render_to_html_string('djue/component.html',
                                     {'form': form})

        js = render_to_js_string('djue/component.js',
                                 {'form': form, 'app': self.app,
                                  'model': self.model, 'self': self})

        return self.render_sfc(html, js)


class TemplateComponent(CrudComponent):
    obj: Template

    def __init__(self, template: Template, *args, **kwargs):
        self.template = template
        super().__init__(*args, **kwargs)

    def render(self):
        html = self.template.source
        js = render_to_js_string('djue/template_component.js', {})

        return self.render_sfc(html, js)


class StaticComponent(Component):
    is_shared = True
    template_name: str
    context: {}

    def __init__(self, template_name: str, context: {} = None, *args,
                 **kwargs):
        self.template_name = template_name
        self.context = {} if context is None else context

        super().__init__(*args, **kwargs)

    def render(self):
        return render_to_string(self.template_name, self.context)

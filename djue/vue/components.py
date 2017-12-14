#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import Template
from django.template.loader import render_to_string

from djue.utils import render_to_html_string, render_to_js_string
from djue.vue.core import SingleFileComponent


class Component(SingleFileComponent):
    dir: str = 'components'


class AnonComponent(Component):
    def render(self):
        html = ''
        js = render_to_js_string('djue/template_component.js', {})

        return self.render_sfc(html, js)


class FormComponent(Component):
    def __init__(self, form, model, *args, **kwargs):
        self.form = form
        self.model = model

        super().__init__(*args, **kwargs)

    def render(self):
        form = self.form

        html = render_to_html_string('djue/component.html',
                                     {'form': form})

        js = render_to_js_string('djue/component.js',
                                 {'form': form, 'app': self.app,
                                  'model': self.model})

        return self.render_sfc(html, js)


class TemplateComponent(Component):
    obj: Template

    def __init__(self, template: Template, *args, **kwargs):
        self.template = template
        super().__init__(*args, **kwargs)

    def render(self):
        html = self.template.source
        js = render_to_js_string('djue/template_component.js', {})

        return self.render_sfc(html, js)


class SharedComponent(Component):
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

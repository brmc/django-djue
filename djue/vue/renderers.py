#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Type

from django.template.loader import render_to_string

from djue import render_to_js_string, render_to_html_string


class Renderer(ABC):
    template: str

    def __init__(self, *args, **kwargs):
        self.context: {} = {}
        super().__init__(*args, **kwargs)

    @abstractmethod
    def render(self):
        pass

    def add_context(self, context):
        self.context.update(context)


class SFCRenderer(Renderer):
    template = 'djue/sfc.vue'
    js_template: str
    html_template: str

    def render(self):
        js = render_to_js_string(self.js_template, self.context)
        html = render_to_html_string(self.html_template, self.context)

        return render_to_string(self.template, {'html': html, 'js': js})


class PlainJsRenderer(Renderer):
    def render(self):
        return render_to_string(self.template, self.context)


class RenderProxy(ABC):
    renderer_cls: Type[Renderer]

    def __init__(self, *args, **kwargs):
        self.renderer: Renderer = self.renderer_cls()
        super().__init__(*args, **kwargs)

    def add_context(self, context):
        self.renderer.add_context(context)

    def render(self):
        return self.renderer.render()


class SCFMixin(RenderProxy):
    renderer_cls = SFCRenderer
    renderer: SFCRenderer

    def set_templates(self, js, html):
        self.renderer.js_template = js
        self.renderer.html_template = html

    def set_templates_from_path_format(self, string, params):
        file = string.format(*params)
        js = file + '.js'
        html = file + '.html'
        self.set_templates(js, html)


class PlainJsMixin(RenderProxy):
    renderer_cls = PlainJsRenderer

    @property
    def template(self):
        return self.renderer.template

    @template.setter
    def template(self, template):
        self.renderer.template = template
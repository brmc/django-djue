#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from abc import ABC, abstractmethod
from typing import Type

from django.template import loader, Context, Template
from django.template.loader import render_to_string

from djue.utils import render_to_js_string, render_to_html_string


class Renderer(ABC):
    template: str

    def __init__(self):
        self.context: {} = {}

    @abstractmethod
    def render(self):
        pass

    def add_context(self, context):
        self.context.update(context)


class StaticRenderer(Renderer):
    def render(self):
        return render_to_string(self.template, self.context)


class SFCRenderer(Renderer):
    template = 'djue/sfc.vue'
    js_template: str
    html_template: str

    def render(self):
        js = self.render_js()
        html = self.render_html()

        return render_to_string(self.template, {'html': html, 'js': js})

    def render_html(self):
        html = render_to_html_string(self.html_template, self.context)
        return html

    def render_js(self):
        js = render_to_js_string(self.js_template, self.context)
        return js


class CBVRenderer(SFCRenderer):
    def render_html(self):
        # Used in f-string, but pycharm doesn't detect usage.  Don't delete
        obj_name = self.context.get('context_obj_name')
        obj_var = re.compile(f'({obj_name})(\.\w+)')
        any_vars = re.compile('\{\{\s*(\w+)(\.\w+)?\s*\}\}')

        src = loader.get_template(self.html_template).template.source
        src = re.sub(obj_var, '\\1\\2.value', src)
        src = src.replace('{{', '{% verbatim %} {{') \
            .replace('}}', '}} {% endverbatim %}')

        var_names = {x[0] for x in any_vars.findall(src) if x[0] != 'object'}
        self.context['preserved_vars'] = var_names
        template = Template(src)

        return template.render(Context(self.context))

    def render(self):
        """
        This is being overridden because  the order of the rendering is
        important

        :return:
        """
        html = self.render_html()
        js = self.render_js()

        return render_to_string(self.template, {'html': html, 'js': js})


class PlainJsRenderer(Renderer):
    def render(self):
        return render_to_js_string(self.template, self.context)


class RenderProxy(ABC):
    renderer_cls: Type[Renderer]

    def __init__(self, *args, **kwargs):
        self.renderer: Renderer = kwargs.pop('renderer', self.renderer_cls)()
        super().__init__(*args, **kwargs)

    def add_context(self, context):
        self.renderer.add_context(context)

    def render(self):
        return self.renderer.render()


class StaticFileMixin(RenderProxy):
    renderer_cls = StaticRenderer
    renderer: StaticRenderer

    def __init__(self, template, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.renderer.template = template


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

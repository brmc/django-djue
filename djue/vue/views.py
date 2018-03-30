#!/usr/bin/env python
# -*- coding: utf-8 -*-

from djue.utils import render_to_js_string, convert_to_kebab_case, \
    render_to_html_string
from djue.vue.core import SingleFileComponent


class View(SingleFileComponent):
    dir = 'views'

    def __init__(self, components, *args, **kwargs):
        self.components = components

        super().__init__(*args, **kwargs)

    def render(self):
        names = {c.name for c in self.components}
        imports = {x.relative_module_import_string for x in self.components}
        html = render_to_html_string('djue/view.html', {})
        js = render_to_js_string('djue/view.js',
                                 {'names': names,
                                  'self': self,
                                  'imports': imports})

        return self.render_sfc(html, js)

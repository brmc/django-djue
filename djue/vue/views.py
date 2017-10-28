#!/usr/bin/env python
# -*- coding: utf-8 -*-

from djue.utils import render_to_js_string, convert_to_kebab_case
from djue.vue.core import SingleFileComponent


class View(SingleFileComponent):
    dir = 'views'

    def __init__(self, components, *args, **kwargs):
        self.components = components

        super().__init__(*args, **kwargs)

    def render(self):
        tags = {convert_to_kebab_case(c.name) for c in self.components}
        names = {c.name for c in self.components}
        imports = {x.relative_module_import_string for x in self.components}
        html = '\n'.join([f'<{tag}></{tag}>' for tag in tags])

        js = render_to_js_string('djue/view.js',
                                 {'names': names,
                                  'imports': imports})

        return self.render_sfc(html, js)

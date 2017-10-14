#!/usr/bin/env python
# -*- coding: utf-8 -*-

from djue.utils import render_to_js_string
from djue.vue.core import SingleFileComponent


class View(SingleFileComponent):
    dir = 'views'

    def __init__(self, components, *args, **kwargs):
        self.components = components

        super().__init__(*args, **kwargs)

    def render(self):
        names = {c.name for c in self.components}
        imports = {x.relative_module_import_string for x in self.components}
        html = '\n'.join([f'<{name}></{name}>' for name in names])

        js = render_to_js_string('djue/view.js',
                                 {'names': names,
                                  'imports': imports})

        return self.render_sfc(html, js)

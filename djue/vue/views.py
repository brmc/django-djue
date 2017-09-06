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
        html = '\n'.join([f'<{c.name}></{c.name}>' for c in self.components])

        js = render_to_js_string('djue/view.js',
                                 {'components': self.components})

        return self.render_sfc(html, js)

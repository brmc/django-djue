#!/usr/bin/env python
# -*- coding: utf-8 -*-
from djue import SCFMixin, CoreFile, ModuleFile
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


class CoreView(SCFMixin, CoreFile):
    dir: str = 'views'
    file_ext: str = '.vue'
    path_format: str = 'djue/core/views/{}'

    def __init__(self, view, name):
        super().__init__(name)
        self.set_templates_from_path_format(self.path_format, [view])


class ModuleView(SCFMixin, ModuleFile):
    dir: str = 'views'
    file_ext: str = '.vue'
    path_format: str = 'djue/modules/views/{}'

    def __init__(self, view, app, name):
        super().__init__(app, name)
        self.set_templates_from_path_format(self.path_format, [view])
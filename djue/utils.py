#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

import jsbeautifier
from bs4 import BeautifulSoup
from django.apps import apps
from django.conf import settings
from django.template.loader import render_to_string
from editorconfig import PathError


def flatten(lst: []) -> []:
    if not isinstance(lst, (list, tuple)):
        return [lst]

    if not lst:
        return lst

    return flatten(lst[0]) + flatten(lst[1:])


def convert_to_pascalcase(string: str) -> str:
    return "".join(
        [word.capitalize() for word in re.findall(r"[a-zA-Z0-9]+", string)])


def convert_to_camelcase(string: str) -> str:
    string = convert_to_pascalcase(string)

    return string[0].lower() + string[1:]


def convert_to_kebab_case(string: str) -> str:
    return re.sub('(?!^)([A-Z])', r'-\1', string).lower()


def replace(match: str) -> str:
    return ':' + match.groups()[-1]


def render_to_js_string(template: str, context: {}):
    output = render_to_string(template, context)
    options = jsbeautifier.default_options()

    opts_file = getattr(settings, 'EDITOR_CONFIG', '.editorconfig')
    options.brace_style = 'collapse,preserve-inline'
    try:
        jsbeautifier.set_file_editorconfig_opts(opts_file, options)
    except PathError:
        log("No editor config found at: {opts_file}")
        log("Using defaults.")

    return jsbeautifier.beautify(output, opts=options)


def render_to_html_string(template, context):
    # todo find a nicer library to pretty print
    if True:
        output = render_to_string(template, context)
        return output.replace('</label>', '</label>\n')

    output = render_to_string(template, context)
    soup = BeautifulSoup(output, 'html.parser')

    return soup.prettify(None, None)


def as_vue(self):
    for name, field in self.fields.items():
        template: str = field.widget.template_name
        field.widget.template_name = template.replace('django/forms', 'djue')

    return self._html_output(
        normal_row='<div%(html_class_attr)s> %(field)s%('
                   'help_text)s</div>',
        error_row='%s',
        row_ender='</div>',
        help_text_html=' <span class="helptext">%s</span>',
        errors_on_separate_row=True)


def get_app_name(obj):
    try:
        return apps.get_containing_app_config(obj.__module__).name
    except AttributeError:
        log("Object is not part of an app. About to do stupid shit")
        return obj.__module__.split('.')[0]


def convert_file_to_component_name(path):
    file_name = path.split(os.path.sep)[-1]
    return convert_to_pascalcase(file_name.split('.')[0].capitalize())


def log(msg):
    sys.stdout.write(msg)
    sys.stdout.write('\n')


def get_output_path():
    root = getattr(settings, 'DJUE_OUTPUT_DIR', os.getcwd())
    path = os.path.join(root, 'src')
    os.makedirs(path, exist_ok=True)

    return path

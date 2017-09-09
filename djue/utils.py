#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import jsbeautifier
from bs4 import BeautifulSoup
from django.apps import apps
from django.conf import settings
from django.template.loader import render_to_string
from editorconfig import PathError


def flatten(lst):
    if not isinstance(lst, (list, tuple)):
        return [lst]

    if not lst:
        return lst

    return flatten(lst[0]) + flatten(lst[1:])


def convert_to_pascalcase(string: str):
    return "".join([word.capitalize() for word in string.split('_')])


def convert_to_camelcase(string: str):
    string = convert_to_pascalcase(string)

    return string[0].lower() + string[1:]


def replace(match):
    return ':' + match.groups()[-1]


def render_to_js_string(template, context):
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

    return self.as_p()


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

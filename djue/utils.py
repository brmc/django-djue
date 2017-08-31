#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jsbeautifier
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

    try:
        jsbeautifier.set_file_editorconfig_opts(opts_file, options)
    except PathError:
        print("No editor config found at: {opts_file}\n"
              "Using defaults.")

    return jsbeautifier.beautify(output, opts=options)

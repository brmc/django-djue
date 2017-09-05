#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Union

from django.template import loader, TemplateDoesNotExist, Template
from django.views import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import ModelFormMixin

from djue.utils import get_app_name, log
from djue.vue.components import TemplateComponent, FormComponent
from djue.vue.views import ClassBasedView, FunctionalView


class ComponentFactory:
    msg = "Building Vue Components from {} has not yet been " \
          "implemented\nSkipping {}..."

    @staticmethod
    def create_from_callback(callback):
        log("Creating from callback")
        msg = ComponentFactory.msg
        if callback is None:
            log('Something strange happened. NoneType passed as callback. '
                'GTFO!')
            return
        if not hasattr(callback, 'view_class'):
            log(msg.format('functional views', callback.__name__))
            return

        view = callback.view_class()

        return ComponentFactory.create_from_cbv(view)

    @staticmethod
    def create_from_template(template: Union[Template, str, list, tuple], app):
        log('This might fail...')
        if isinstance(template, (list, tuple)):
            log('Selecting template from template candidates')
            template = loader.select_template(template).template
        elif isinstance(template, str):
            log('Loading explicit template')
            template = loader.get_template(template).template

        log('Creating component from template')

        template = TemplateComponent(template, app)

        log('I was wrong! Success!')

        return template

    @staticmethod
    def create_from_form(form_class):
        log('Creating form component')
        return FormComponent(form_class)

    @staticmethod
    def create_from_cbv(view: View):
        log(f'Creating from CBV: {view.__module__}.{view.__class__}')
        if isinstance(view, ModelFormMixin):

            form_class = view.get_form_class()

            return ComponentFactory.create_from_form(form_class)
        elif isinstance(view, TemplateResponseMixin):
            # workaround for state variance. No default value is set for object
            # django/views/generic/detail.py:144
            # django 1.11

            if hasattr(view, 'model'):
                view.object = None
                view.object_list = view.model.objects.all()

            app = get_app_name(view)
            try:
                return ComponentFactory.create_from_template(
                    view.get_template_names(), app)
            except TemplateDoesNotExist:
                log('Failed! Hacking template together!')
                name = view.get_template_names()[0]
                template = Template('You must create a template')
                template.name = name
                return ComponentFactory.create_from_template(template, app)


class ViewFactory:
    @staticmethod
    def create_from_callback(callback):
        components = [ComponentFactory.create_from_callback(callback)]

        if hasattr(callback, 'view_class'):
            return ClassBasedView(callback, components)
        else:
            return FunctionalView(callback, components)
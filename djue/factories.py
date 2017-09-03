#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import BaseListView

from djue.vue import FormComponent


class ComponentFactory:
    @staticmethod
    def create_from_callback(callback):
        msg = "not implemented for {}: {}\nskipping..."

        if callback is None:
            sys.stdout.write(
                'Something strange happened. NoneType passed as callback\n')
            return
        if not hasattr(callback, 'view_class'):
            sys.stdout.write(msg.format('functional views', callback.__name__))
            return

        view = callback.view_class()

        if isinstance(view, ModelFormMixin):
            form_class = view.get_form_class()

            return ComponentFactory.create_from_form(form_class)
        elif isinstance(view, (BaseListView, BaseDetailView)):
            ComponentFactory.create_from_template(callback, msg)

    @staticmethod
    def create_from_template(callback, msg):
        sys.stdout.write('detail views not implemented: \n')
        sys.stdout.write(msg.format("detail views", callback.__name__))

    @staticmethod
    def create_from_form(form_class):
        return FormComponent(form_class)

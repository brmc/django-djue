#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Union, Type

from django.forms import ModelForm, modelform_factory
from django.template import loader, TemplateDoesNotExist, Template
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import ModelFormMixin
from rest_framework.routers import APIRootView
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from djue.utils import get_app_name, log, as_vue, \
    convert_file_to_component_name, convert_to_camelcase, convert_to_pascalcase
from djue.vue.components import TemplateComponent, FormComponent, \
    AnonComponent, SharedComponent
from djue.vue.views import View
from djue.vue.vuex import Store


class ComponentFactory:
    msg = "Building Vue Components from {} has not yet been " \
          "implemented\nSkipping {}..."

    @staticmethod
    def create_anonymous_component(app, name):
        return AnonComponent(app, name)

    @staticmethod
    def create_from_callback(callback):
        log("Creating from callback")
        if callback is None:
            log('Something strange happened. NoneType passed as callback. '
                'GTFO!')
            return

        if hasattr(callback, 'cls'):
            return ComponentFactory.create_from_drf_class(callback.cls)

        if not hasattr(callback, 'view_class'):
            name = callback.__name__
            app = get_app_name(callback)

            log(f'Creating Anonymous component for functional view: {name}')
            return ComponentFactory.create_anonymous_component(app, name)

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
        name = convert_file_to_component_name(template.name) + 'Template'

        template = TemplateComponent(template, app, name)

        log('I was wrong! Success!')

        return template

    @staticmethod
    def create_from_form(form_class):
        log('Creating form_class component')
        form_class.as_vue = as_vue
        name = form_class.__name__
        model = form_class._meta.model.__name__
        app = get_app_name(form_class)

        return FormComponent(form_class(), model, app, name)

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
                template = Template('<div>You must create a template</div>')
                template.name = name
                return ComponentFactory.create_from_template(template, app)

    @staticmethod
    def create_from_drf_class(cls):
        log(f'Creating from DRF class: {cls.__name__}')
        obj = cls()

        if isinstance(obj, ModelViewSet):
            serializer = obj.get_serializer_class()

            return ComponentFactory.create_from_serializer(serializer)

        if isinstance(obj, APIRootView):
            return SharedComponent('djue/raw/APIRootView.vue',
                                   app='',
                                   name='APIRootView')

    @staticmethod
    def create_from_serializer(serializer):
        model = serializer.Meta.model
        fields = serializer.Meta.fields
        form_class = modelform_factory(model, fields=fields)
        app = get_app_name(serializer)

        form_class.as_vue = as_vue
        name = serializer.__name__

        return FormComponent(form_class(), model.__name__, app, name)

    @staticmethod
    def create_from_junk(callback, method, action):
        app = get_app_name(callback)
        name = convert_to_pascalcase(
            action) + callback.cls.__name__ + 'Component'

        form_methods = ['post', 'put', 'patch']

        if method in form_methods:
            serializer = callback.cls.serializer_class
            return ComponentFactory.create_from_serializer(serializer)
        else:
            return ComponentFactory.create_anonymous_component(app, name)


class ViewFactory:
    @staticmethod
    def create_from_callback(callback):
        if hasattr(callback, 'actions'):
            return ViewFactory.create_from_viewset(callback)

        components = [ComponentFactory.create_from_callback(callback)]
        app = get_app_name(callback)

        if components in [[None], []]:
            log(f'No component generated for {callback.__name__}')
            return
        if hasattr(callback, 'view_class'):
            name = callback.view_class.__name__
        else:
            name = convert_to_camelcase(callback.__name__)

        return View(components, app, name)

    @staticmethod
    def create_from_view(view):
        name = view.__name__
        app = get_app_name(view)
        components = [ComponentFactory.create_from_cbv(view)]

        return View(components, app, name)

    @staticmethod
    def create_from_viewset(viewset):
        name = viewset.cls.__name__ + viewset.suffix
        app = get_app_name(viewset)

        components = [
            ComponentFactory.create_from_junk(viewset, method, action) for
            method, action in viewset.actions.items()]

        return View(components, app, name)


class StoreFactory:
    @staticmethod
    def create_from_model_and_fields(model, fields):
        props = []
        for name, field in fields.items():
            f = model._meta.get_field(name)
            validators = [v.__class__.__name__ for v in f.validators]
            f.validator_names = validators
            props.append(f)

        app = get_app_name(model)

        return Store(app, model.__name__, props)

    @staticmethod
    def create_from_form(form: Type[ModelForm]):
        model = form._meta.model
        fields = form().fields

        return StoreFactory.create_from_model_and_fields(model, fields)

    @staticmethod
    def create_from_serializer(serializer: Type[ModelSerializer]):
        model = serializer.Meta.model
        fields = serializer().fields

        return StoreFactory.create_from_model_and_fields(model, fields)

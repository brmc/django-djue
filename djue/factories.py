#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Type

from django.db.models import Model
from django.forms import ModelForm, modelform_factory
from django.template import loader, TemplateDoesNotExist
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import ModelFormMixin
from rest_framework.routers import APIRootView
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from djue.utils import get_app_name, log, as_vue, \
    convert_file_to_component_name, convert_to_camelcase, convert_to_pascalcase
from djue.vue.base import StaticFile
from djue.vue.components import AnonComponent, ModuleComponent
from djue.vue.views import View
from djue.vue.vuex import Store


class ComponentFactory:
    msg = "Building Vue Components from {} has not yet been " \
          "implemented\nSkipping {}..."

    @classmethod
    def create_anonymous_component(cls, app, name, action):
        return AnonComponent(action, app, name)

    @classmethod
    def from_callback(cls, callback):
        log("Creating from callback")
        if callback is None:
            log('Something strange happened. NoneType passed as callback. '
                'GTFO!')
            return

        if not hasattr(callback, 'view_class'):
            name = callback.__name__
            app = get_app_name(callback)

            log(f'Creating Anonymous component for functional view: {name}')
            return ModuleComponent('generic', app, name)

        view = callback.view_class()

        if isinstance(view, APIView):
            return cls.from_drf_view(view)

        return cls.from_cbv(view)

    @classmethod
    def from_template(cls, view):
        model = ''
        # workaround for state variance. No default value is set for object
        # django/views/generic/detail.py:144
        # django 1.11
        if hasattr(view, 'model'):
            view.object = None
            view.object_list = view.model.objects.all()
            model = view.model.__name__

        app = get_app_name(view)
        candidates = view.get_template_names()

        use_generic_html = True
        try:
            template_path = loader.select_template(candidates).template.name
            use_generic_html = False
            log('Creating component from template:')
        except TemplateDoesNotExist:
            log('No Template found. Blindly creating component from first '
                'template candidate')
            template_path = candidates[0]

        name = convert_file_to_component_name(template_path)
        component = ModuleComponent('generic', app, name)

        model and component.add_context({'model': model})

        if not use_generic_html:
            component.renderer.html_template = template_path

        return component

    @classmethod
    def from_form(cls, form_class):
        log('Creating form_class component')
        form_class.as_vue = as_vue
        name = form_class.__name__
        model = form_class._meta.model.__name__
        app = get_app_name(form_class)

        component = ModuleComponent('component', app, name)
        component.add_context({
            'model': model,
            'form': form_class()
        })
        return component

    @classmethod
    def from_cbv(cls, view: View):
        log(f'Creating from CBV: {view.__module__}.{view.__class__}')
        form = None
        if isinstance(view, ModelFormMixin):
            form_class = view.get_form_class()
            form = cls.from_form(form_class)

        if isinstance(view, TemplateResponseMixin):
            component = cls.from_template(view)
        else:
            component = ModuleComponent('generic',
                                        get_app_name(view),
                                        view.__class__.__name__)

        if hasattr(view, 'model'):
            component.add_context({'model': view.model.__name__})
        return component, form

    @classmethod
    def from_drf_view(cls, view):
        log(f'Creating from DRF class: {view}')

        if isinstance(view, ModelViewSet):
            serializer = view.get_serializer_class()

            return cls.from_serializer(serializer)

        if isinstance(view, APIRootView):
            return StaticFile(template='djue/raw/APIRootView.vue',
                              output_path='modules/rest_framework/components')

        raise Exception(
            'Sumpin done screwed up while trying to create a component from a'
            'DRF class. It is not your fault though (unless you are me). the '
            'stupid author of this library clearly is aware of the this case. '
            'Hell, it is not even an edge case. it is a common scenario for '
            'anyone using basic DRF APIViews. I will get around to it soon')

    @classmethod
    def from_serializer(cls, serializer):
        model = serializer.Meta.model
        fields = serializer.Meta.fields
        form_class = modelform_factory(model, fields=fields)
        app = get_app_name(serializer)

        form_class.as_vue = as_vue
        name = serializer.__name__

        form = ModuleComponent('component', app, name)
        form.add_context({
            'form': form_class(),
            'model': model.__name__
        })

        return form

    @classmethod
    def from_junk(cls, callback, method, action):
        app = get_app_name(callback)
        action_cls = convert_to_pascalcase(action)
        model = callback.cls.__name__
        name = model + action_cls + 'Component'

        form_methods = ['post', 'put', 'patch']
        serializer = callback.cls.serializer_class

        if method in form_methods:
            form = cls.from_serializer(serializer)
        else:
            form = None

        model = serializer.Meta.model.__name__
        comp = ModuleComponent(action, app, name)
        comp.add_context({
            'model': model,
            'component': form
        })

        return comp, form


class ViewFactory:
    @classmethod
    def from_callback(cls, callback):
        if hasattr(callback, 'actions'):
            return cls.from_viewset(callback)

        components = [ComponentFactory.from_callback(callback)]
        app = get_app_name(callback)

        if components in [[None], []]:
            log(f'No component generated for {callback.__name__}')
            return
        if hasattr(callback, 'view_class'):
            name = callback.view_class.__name__
        else:
            name = convert_to_camelcase(callback.__name__)

        return View(components, app, name)

    @classmethod
    def from_view(cls, view):
        name = view.__name__
        app = get_app_name(view)
        components = [ComponentFactory.from_cbv(view)]

        return View(components, app, name)

    @classmethod
    def from_viewset(cls, viewset):
        name = viewset.cls.__name__ + viewset.suffix
        app = get_app_name(viewset)

        components = [
            ComponentFactory.from_junk(viewset, method, action)[0] for
            method, action in viewset.actions.items()]

        return View(components, app, name)


class StoreFactory:
    @classmethod
    def from_model_and_fields(cls, model: Model, fields):
        props = []
        for name, field in fields.items():
            f = model._meta.get_field(name)
            validators = [v.__class__.__name__ for v in f.validators]
            f.validator_names = validators
            props.append(f)

        app = get_app_name(model)

        return Store(app, model.__name__, props)

    @classmethod
    def from_form(cls, form: Type[ModelForm]):
        model = form._meta.model
        fields = form().fields

        return cls.from_model_and_fields(model, fields)

    @classmethod
    def from_serializer(cls, serializer: Type[ModelSerializer]):
        model = serializer.Meta.model
        fields = serializer().fields

        return cls.from_model_and_fields(model, fields)

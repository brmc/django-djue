# -*- coding: utf-8 -*-
from django import forms
from django.http import JsonResponse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)
from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer

from .models import (
    Example,
    ExampleForm)


class F(forms.Form):
    pass


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            safe=False,
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """

        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.

        context = [x.__dict__ for x in context['object_list']]
        return context


class ExampleCreateView(JSONResponseMixin, CreateView):
    model = Example
    template_name = 'app/create.html'
    form_class = ExampleForm

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class ExampleDeleteView(JSONResponseMixin, DeleteView):
    model = Example

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class ExampleDetailView(JSONResponseMixin, DetailView):
    model = Example
    template_name = 'djue/detail.html'

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class ExampleUpdateView(JSONResponseMixin, UpdateView):
    model = Example
    form_class = ExampleForm

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class ExampleListView(JSONResponseMixin, ListView):
    model = Example

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

class ExampleSerializer(ModelSerializer):
    class Meta:
        model = Example
        fields = ['id', 'name', 'description']


class ExampleViewSet(viewsets.ModelViewSet):
    serializer_class = ExampleSerializer
    queryset = Example.objects.all()

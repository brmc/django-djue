# -*- coding: utf-8 -*-
from django import forms
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
    Example,
)


class F(forms.Form):
    pass


class ExampleCreateView(CreateView):
    model = Example
    fields = ('name', 'description')


class ExampleDeleteView(DeleteView):
    model = Example


class ExampleDetailView(DetailView):
    model = Example
    template_name = 'djue/detail.html'


class ExampleUpdateView(UpdateView):
    model = Example


class ExampleListView(ListView):
    model = Example


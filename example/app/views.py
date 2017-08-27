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
    fields = ('a', 't')
    model = Example


class ExampleDeleteView(DeleteView):
    model = Example


class ExampleDetailView(DetailView):
    model = Example


class ExampleUpdateView(UpdateView):
    model = Example


class ExampleListView(ListView):
    model = Example


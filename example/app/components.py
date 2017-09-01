#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin

from .views import ExampleCreateView

urlpatterns = [
    url(r'^x/', ExampleCreateView.as_view()),
]

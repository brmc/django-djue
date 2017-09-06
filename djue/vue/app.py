#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from django.views import View

from djue.vue.aux import Router, Store, Route


class Module:
    routes: List[Route]
    

class App:
    router: Router
    store: Store
    views: List[View]
    components: List[View]
    modules: []

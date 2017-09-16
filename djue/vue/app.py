#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from django.views import View

from djue.vue.vuex import Store
from djue.vue.routers import Route, Router


class Module:
    routes: List[Route]
    

class App:
    router: Router
    store: Store
    views: List[View]
    components: List[View]
    modules: []

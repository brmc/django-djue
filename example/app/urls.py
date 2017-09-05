# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
class T(TemplateView):
    template_name = 'app/create.html'

urlpatterns = [
    url(
        '/?',
        view=T.as_view(),
    ),
    url(
        regex="^Example/~create/$",
        view=views.ExampleCreateView.as_view(),
        name='Example_create',
    ),
    url(
        regex="^Example/(?P<pk>\d+)/~delete/$",
        view=views.ExampleDeleteView.as_view(),
        name='Example_delete',
    ),
    url(
        regex="^Example/(?P<pk>\d+)/$",
        view=views.ExampleDetailView.as_view(),
        name='Example_detail',
    ),
    url(
        regex="^Example/(?P<pk>\d+)/~update/$",
        view=views.ExampleUpdateView.as_view(),
        name='Example_update',
    ),
    url(
        regex="^Example/$",
        view=views.ExampleListView.as_view(),
        name='Example_list',
    ),
]

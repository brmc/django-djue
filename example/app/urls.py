# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views

class Index(TemplateView):
    template_name = 'index.html'

router = DefaultRouter()
router.register('examples', views.ExampleViewSet)

app_name = 'app'

urlpatterns = url('', include(router.urls, app_name='app', namespace='api'), name='api'),
lurlpatterns = [
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
        regex="^Example",
        view=views.ExampleListView.as_view(),
        name='Example_list',
    ),
    url(
        '$',
        view=Index.as_view(),
    ),
]

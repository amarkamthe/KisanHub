from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'celery_try.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', (views.IndexView).as_view(),name='index'),
    url(r'^analysis/(?P<component>[0-9]+)$', views.analysis, name='rainfall_analysis'),
    url(r'^analysis_data/(?P<component>[0-9]+)/(?P<region>[0-9]+)/$', views.rainfall, name='rainfall'),
    url(r'^temperature/(?P<component>[0-9]+)$', views.temperature_analysis, name='temperature_analysis'),

]

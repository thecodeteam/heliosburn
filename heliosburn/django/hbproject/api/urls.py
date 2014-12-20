from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^version$', views.version),
)

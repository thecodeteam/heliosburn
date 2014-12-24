from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    'webui.views',
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^signin/$', 'signin', name='signin'),
    url(r'^sessions/$', 'session_manager', name='session_manager'),
    url(r'^sessions/(?P<id>[\w-]+)$', 'session_details', name='session_details'),
)
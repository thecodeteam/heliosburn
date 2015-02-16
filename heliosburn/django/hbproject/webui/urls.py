from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    'webui.views',
    url(r'^$', 'dashboard', name='dashboard'),

    url(r'^signin/$', 'signin', name='signin'),
    url(r'^signout/$', 'signout', name='signout'),

    url(r'^sessions/$', 'session_list', name='session_list'),
    url(r'^sessions/(?P<id>[\w-]+)$', 'session_details', name='session_details'),
    url(r'^sessions/update/$', 'session_update', name='session_update'),
    url(r'^sessions/new/step-(?P<step>[\w-]+)$', 'session_new', name='session_new'),
    url(r'^sessions/(?P<id>[\w-]+)/execute$', 'session_execution', name='session_execution'),

    url(r'^executions/(?P<id>[\w-]+)$', 'execution_details', name='execution_details'),

    url(r'^testplans/$', 'testplan_list', name='testplan_list'),
    url(r'^testplans/(?P<id>[\w-]+)$', 'testplan_details', name='testplan_details'),
    url(r'^testplans/update/$', 'testplan_update', name='testplan_update'),
    url(r'^testplans/new/$', 'testplan_new', name='testplan_new'),
    url(r'^testplans/delete/$', 'testplan_delete', name='testplan_delete'),

    url(r'^testplans/(?P<testplan_id>[\w-]+)/rules/(?P<rule_id>[\w-]+)$', 'rule_details', name='rule_details'),

    url(r'^recordings/$', 'recording_list', name='recording_list'),
    url(r'^recordings/(?P<id>[\w-]+)$', 'recording_details', name='recording_details'),
    url(r'^recordings/update/$', 'recording_update', name='recording_update'),

    url(r'^ajax/traffic/$', 'ajax_traffic', name='ajax_traffic'),

    url(r'^settings/$', 'settings_view', name='settings'),
)
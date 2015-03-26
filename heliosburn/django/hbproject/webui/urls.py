from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from webui.views.dashboard import DashboardView
from webui.views.login import LoginView

urlpatterns = patterns(
    'webui.views',
    url(r'^$', DashboardView.as_view(), name='dashboard'),

    url(r'^signin/$', LoginView.as_view(), name='signin'),
    url(r'^signout/$', 'signout', name='signout'),

    url(r'^sessions/$', 'session.session_list', name='session_list'),
    url(r'^sessions/(?P<id>[\w-]+)$', 'session.session_details', name='session_details'),
    url(r'^sessions/update/$', 'session.session_update', name='session_update'),
    url(r'^sessions/new/step-(?P<step>[\w-]+)$', 'session.session_new', name='session_new'),
    url(r'^sessions/(?P<id>[\w-]+)/execute$', 'session.session_execution', name='session_execution'),

    url(r'^executions/(?P<id>[\w-]+)$', 'execution_details', name='execution_details'),

    url(r'^testplans/$', 'testplan.testplan_list', name='testplan_list'),
    url(r'^testplans/(?P<testplan_id>[\w-]+)$', 'testplan.testplan_details', name='testplan_details'),
    url(r'^testplans/update/$', 'testplan.testplan_update', name='testplan_update'),
    url(r'^testplans/new/$', 'testplan.testplan_new', name='testplan_new'),
    url(r'^testplans/delete/$', 'testplan.testplan_delete', name='testplan_delete'),

    url(r'^testplans/(?P<testplan_id>[\w-]+)/rules/(?P<rule_id>[\w-]+)$', 'rule.rule_details', name='rule_details'),
    url(r'^testplans/(?P<testplan_id>[\w-]+)/rules/(?P<rule_id>[\w-]+)/update$', 'rule.rule_update', name='rule_update'),
    url(r'^testplans/(?P<testplan_id>[\w-]+)/rules/new/$', 'rule.rule_new', name='rule_new'),

    url(r'^recordings/$', 'recording.recording_list', name='recording_list'),
    url(r'^recordings/(?P<recording_id>[\w-]+)$', 'recording.recording_details', name='recording_details'),
    url(r'^recordings/(?P<recording_id>[\w-]+)/live$', 'recording.recording_live', name='recording_live'),
    url(r'^recordings/(?P<recording_id>[\w-]+)/start$', 'recording.recording_start', name='recording_start'),
    url(r'^recordings/(?P<recording_id>[\w-]+)/stop$', 'recording.recording_stop', name='recording_stop'),
    url(r'^recordings/update/$', 'recording.recording_update', name='recording_update'),
    url(r'^recordings/new/$', 'recording.recording_new', name='recording_new'),

    url(r'^ajax/traffic/$', 'ajax_traffic', name='ajax_traffic'),

    url(r'^settings/$', 'settings_view', name='settings'),
)
from django.conf.urls import patterns, url
from webui.views.dashboard import DashboardView
from webui.views.login import LoginView
from webui.views.logs import LogsView

urlpatterns = patterns(
    'webui.views',
    url(r'^$', DashboardView.as_view(), name='dashboard'),

    url(r'^signin/$', LoginView.as_view(), name='signin'),
    url(r'^signout/$', 'signout', name='signout'),

    url(r'^sessions/$', 'session.session_list', name='session_list'),
    url(r'^sessions/(?P<session_id>[\w-]+)$', 'session.session_details', name='session_details'),
    url(r'^sessions/update/$', 'session.session_update', name='session_update'),
    url(r'^sessions/new/$', 'session.session_new', name='session_new'),
    url(r'^sessions/create/$', 'session.session_create', name='session_create'),
    url(r'^sessions/(?P<session_id>[\w-]+)/execute$', 'session.session_execute', name='session_execute'),

    url(r'^sessions/(?P<session_id>[\w-]+)/start', 'session.session_start', name='session_start'),
    url(r'^sessions/(?P<session_id>[\w-]+)/stop', 'session.session_stop', name='session_stop'),

    url(r'^sessions/(?P<session_id>[\w-]+)/executions/(?P<execution_id>[\w-]+)$', 'execution_details', name='execution_details'),

    url(r'^testplans/$', 'testplan.testplan_list', name='testplan_list'),
    url(r'^testplans/(?P<testplan_id>[\w-]+)$', 'testplan.testplan_details', name='testplan_details'),
    url(r'^testplans/update/$', 'testplan.testplan_update', name='testplan_update'),
    url(r'^testplans/new/$', 'testplan.testplan_new', name='testplan_new'),
    url(r'^testplans/delete/$', 'testplan.testplan_delete', name='testplan_delete'),

    url(r'^testplans/(?P<testplan_id>[\w-]+)/rules/(?P<rule_id>[\w-]+)$', 'rule.rule_details', name='rule_details'),
    url(r'^testplans/(?P<testplan_id>[\w-]+)/rules/(?P<rule_id>[\w-]+)/update$', 'rule.rule_update', name='rule_update'),
    url(r'^testplans/(?P<testplan_id>[\w-]+)/rules/new/$', 'rule.rule_new', name='rule_new'),

    url(r'^qos/$', 'qos.qos_list', name='qos_list'),
    url(r'^qos/(?P<qos_id>[\w-]+)$', 'qos.qos_details', name='qos_details'),
    url(r'^qos/update/$', 'qos.qos_update', name='qos_update'),
    url(r'^qos/new/$', 'qos.qos_new', name='qos_new'),
    url(r'^qos/delete/$', 'qos.qos_delete', name='qos_delete'),

    url(r'^serveroverload/$', 'serveroverload.serveroverload_list', name='serveroverload_list'),
    url(r'^serveroverload/(?P<serveroverload_id>[\w-]+)$', 'serveroverload.serveroverload_details', name='serveroverload_details'),
    url(r'^serveroverload/update/$', 'serveroverload.serveroverload_update', name='serveroverload_update'),
    url(r'^serveroverload/new/$', 'serveroverload.serveroverload_new', name='serveroverload_new'),
    url(r'^serveroverload/delete/$', 'serveroverload.serveroverload_delete', name='serveroverload_delete'),

    url(r'^recordings/$', 'recording.recording_list', name='recording_list'),
    url(r'^recordings/(?P<recording_id>[\w-]+)$', 'recording.recording_details', name='recording_details'),
    url(r'^recordings/(?P<recording_id>[\w-]+)/live$', 'recording.recording_live', name='recording_live'),
    url(r'^recordings/(?P<recording_id>[\w-]+)/start$', 'recording.recording_start', name='recording_start'),
    url(r'^recordings/(?P<recording_id>[\w-]+)/stop$', 'recording.recording_stop', name='recording_stop'),
    url(r'^recordings/update/$', 'recording.recording_update', name='recording_update'),
    url(r'^recordings/new/$', 'recording.recording_new', name='recording_new'),

    url(r'^ajax/traffic/$', 'ajax_traffic', name='ajax_traffic'),

    url(r'^logs/$', LogsView.as_view(), name='logs'),

    url(r'^settings/$', 'settings_view', name='settings'),
)
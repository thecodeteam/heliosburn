from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.core.urlresolvers import reverse
import json


def signin(request):
    return render(request, 'signin.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def session_list(request):
    sessions = [
        {
            'id': 1,
            'name': 'Session A',
            'testplan':
                {
                    'id': 12,
                    'name': 'ViPR Test plan'
                },
            'executions': 42,
            'latest_execution_at': '2014-02-12 03:34:51'
        },
        {
            'id': 2,
            'name': 'ViPR Session 1',
            'testplan':
                {
                    'id': 12,
                    'name': 'ViPR Test plan'
                },
            'executions': 634,
            'latest_execution_at': '2014-02-12 03:34:51'
        },
        {
            'id': 3,
            'name': 'ViPR Session 2',
            'testplan':
                {
                    'id': 12,
                    'name': 'ViPR Test plan'
                },
            'executions': 341,
            'latest_execution_at': '2014-02-12 03:34:51'
        },
        {
            'id': 4,
            'name': 'Swift on-premise session',
            'testplan':
                {
                    'id': 12,
                    'name': 'Swift Test plan'
                },
            'executions': 654,
            'latest_execution_at': '2014-02-12 03:34:51'
        },
        {
            'id': 5,
            'name': 'S3 America session',
            'testplan':
                {
                    'id': 12,
                    'name': 'Amazon S3 Test plan'
                },
            'executions': 244,
            'latest_execution_at': '2014-02-12 03:34:51'
        }
    ]

    args = {}
    args['sessions'] = sessions

    return render(request, 'sessions/session_list.html', args)


def session_details(request, id):
    return render(request, 'sessions/session_details.html')


def testplan_list(request):
    data = [
        {
            'id': 1,
            'name': 'Amazon S3 Test Plan',
            'description': 'My test plan for Amazon S3...',
            'rules': 42,
            'updated_at': '2014-02-12 03:34:51'
        },
        {
            'id': 2,
            'name': 'Test Plan for Swift',
            'description': 'bla bla bla bla bla blaaaa...',
            'rules': 654,
            'updated_at': '2014-02-12 03:34:51'
        },
        {
            'id': 3,
            'name': 'EMC ViPR Test Plan',
            'description': 'bla bla bla bla bla blaaaa...',
            'rules': 34,
            'updated_at': '2014-02-12 03:34:51'
        },
        {
            'id': 4,
            'name': 'Test Plan for EMC Atmos',
            'description': 'bla bla bla bla bla blaaaa...',
            'rules': 2134,
            'updated_at': '2014-02-12 03:34:51'
        },
    ]

    args = {}
    args['data'] = data

    return render(request, 'testplan/testplan_list.html', args)


def testplan_details(request, id):
    testplan = {
        'id': 4,
        'name': 'Test Plan for EMC Atmos',
        'description': 'bla bla bla bla bla blaaaa...',
        'updated_at': '2014-02-12 03:34:51',
        'created_at': '2014-02-12 03:34:51',
        'latency_enabled': True,
        'client_latency': 100,
        'server_latency': 300,
        'rules': [
            {'id': 1,
             'filter': 'GET, http://asdas.com/safg',
             'action': 'New response',
             'enabled': True,
             'type': 'request'},
            {'id': 2,
             'filter': 'GET, http://asdas.com/safg',
             'action': 'Modify header(X-Storage-URL)="blabla"',
             'enabled': False,
             'type': 'request'},
            {'id': 3,
             'filter': '200, Header="Hello"',
             'action': 'New response',
             'enabled': True,
             'type': 'response'},
            {'id': 4,
             'filter': 'DELETE, http://asdas.com/safg',
             'action': 'Drop connection',
             'enabled': True,
             'type': 'request'},
            {'id': 5,
             'filter': 'GET, http://asdas.com/safg',
             'action': 'New response',
             'enabled': True,
             'type': 'request'},
            {'id': 6,
             'filter': 'GET, http://asdas.com/safg',
             'action': 'New response',
             'enabled': False,
             'type': 'request'},
            {'id': 7,
             'filter': 'GET, http://asdas.com/safg',
             'action': 'New response',
             'enabled': True,
             'type': 'request'},
        ],

    }

    args = {}
    args['testplan'] = testplan

    return render(request, 'testplan/testplan_details.html', args)


def testplan_update(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('testplan_list'))

    name = request.POST.get('name')
    pk = request.POST.get('pk')
    value = request.POST.get('value')

    if not name or not pk:
        response = 'field cannot be empty!'
        return HttpResponseBadRequest(response)
    else:
        # TODO: API call to update value
        return HttpResponse()


def rule_details(request, id):
    rule = {'id': 1,
            'filter': 'GET, http://asdas.com/safg',
            'action': 'New response',
            'enabled': True,
            'type': 'request'}

    args = {}
    args['rule'] = rule

    return render(request, 'testplan/rule_details.html', args)


def recording_list(request):
    recordings = [
        {
            'id': 1,
            'name': 'Recording 1',
            'description': 'My recording bla bla bla...',
            'requests': 42,
            'created_at': '2014-02-12 03:34:51'
        },
        {
            'id': 2,
            'name': 'Recording 2',
            'description': 'My recording bla bla bla...',
            'requests': 23,
            'created_at': '2014-02-12 03:34:51'
        },
        {
            'id': 3,
            'name': 'Recording 3',
            'description': 'My recording bla bla bla...',
            'requests': 2,
            'created_at': '2014-02-12 03:34:51'
        },
        {
            'id': 4,
            'name': 'Recording 4',
            'description': 'My recording bla bla bla...',
            'requests': 442,
            'created_at': '2014-02-12 03:34:51'
        },
        {
            'id': 5,
            'name': 'Recording 5',
            'description': 'My recording bla bla bla...',
            'requests': 345,
            'created_at': '2014-02-12 03:34:51'
        },
        {
            'id': 6,
            'name': 'Recording 6',
            'description': 'My recording bla bla bla...',
            'requests': 93,
            'created_at': '2014-02-12 03:34:51'
        },
        {
            'id': 7,
            'name': 'Recording 7',
            'description': 'My recording bla bla bla...',
            'requests': 12,
            'created_at': '2014-02-12 03:34:51'
        },
    ]

    args = {}
    args['recordings'] = recordings

    return render(request, 'recording/recording_list.html', args)


def recording_details(request, id):
    recording = {
        'id': 1,
        'name': 'Recording 1',
        'description': 'My recording bla bla bla...',
        'created_at': '2014-02-12 03:34:51',
        'duration': 343,
        'traffic': [
            {
                'id': 23,
                'method': 'GET',
                'url': 'http://asdasdasd.com/ikdsf',
                'date': '2014-02-12 03:34:51',
                'response': {
                    'status_code': 200
                }
            },
            {
                'id': 43,
                'method': 'GET',
                'url': 'http://asdasdasd.com/ikdsf',
                'date': '2014-02-12 03:34:51',
                'response': {
                    'status_code': 200
                }
            },
            {
                'id': 54,
                'method': 'GET',
                'url': 'http://asdasdasd.com/ikdsf',
                'date': '2014-02-12 03:34:51',
                'response': {
                    'status_code': 500
                }
            },
            {
                'id': 87,
                'method': 'GET',
                'url': 'http://asdasdasd.com/ikdsf',
                'date': '2014-02-12 03:34:51',
                'response': {
                    'status_code': 200
                }
            }
        ]
    }

    args = {}
    args['recording'] = recording

    return render(request, 'recording/recording_details.html', args)


def recording_update(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('recording_list'))

    name = request.POST.get('name')
    pk = request.POST.get('pk')
    value = request.POST.get('value')

    if not name or not pk:
        response = 'field cannot be empty!'
        return HttpResponseBadRequest(response)
    else:
        # TODO: API call to update value
        return HttpResponse()
from django.shortcuts import render


def signin(request):
    return render(request, 'signin.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def session_list(request):
    return render(request, 'sessions/list.html')


def session_details(request):
    return render(request, 'sessions/list.html')


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

    return render(request, 'testplan/list.html', args)


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

    return render(request, 'testplan/details.html', args)


def rule_details(request, id):
    rule = {'id': 1,
            'filter': 'GET, http://asdas.com/safg',
            'action': 'New response',
            'enabled': True,
            'type': 'request'}

    args = {}
    args['rule'] = rule

    return render(request, 'testplan/rule_details.html', args)
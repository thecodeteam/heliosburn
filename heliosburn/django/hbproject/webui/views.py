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


def testplan_details(request):
    return render(request, 'testplan/list.html')
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.conf import settings
import requests
import json
import random
import datetime


MOCK_PROTOCOL = "http"
MOCK_HOST = "127.0.0.1"
MOCK_PORT = "8000"

WIZARD_STEPS = ['1', '2', '3', '4']


def signin(request):

    if not request.POST:
        return render(request, 'signin.html')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    if not username or not password:
        messages.error(request, 'Invalid login credentials')
        return render(request, 'signin.html')

    try:
        user = auth.authenticate(username=username, password=password)
    except Exception as inst:
        messages.error(request, 'Something went wrong.')
        return render(request, 'signin.html')

    if not user:
        messages.error(request, 'Invalid login credentials')
        return render(request, 'signin.html')

    auth.login(request, user)
    redirect_url = request.GET.get('next', reverse('dashboard'))
    return HttpResponseRedirect(redirect_url)


def signout(request):
    auth.logout(request)
    return redirect(reverse('signin'))


@login_required
def dashboard(request):
    args = {}
    args['maxRequests'] = 20

    return render(request, 'dashboard.html', args)


@login_required
def ajax_traffic(request):
    methods = ['GET', 'PUT', 'DELETE', 'POST']
    statuses = [('200', 'OK'),
                ('204', 'No Content'),
                ('404', 'Not Found'),
                ('201', 'Created'),
                ('500', 'Internal Server Error')]
    urls = [
        'http://example.com/api/resource1/ob543',
        'http://example.com/api/account3/',
        'http://example.com/api/acco955/mycontainer0092',
        'http://example.com/api/acco955/mycontainer5/file.txt',
        'http://example.com/api/myacc/asdfg/dfofdg.mp3',
        'http://example.com/api/testaccount/testcontainer/helios.zip',
        'http://example.com/api/default_account/default_container'
    ]
    now = datetime.datetime.now()
    now.strftime('%Y-%m-%d %H:%M:%S')

    data = {}
    data['count'] = random.randint(0, 3)
    data['more'] = False
    data['requests'] = []

    for i in range(data['count']):
        request = {}
        request['id'] = i
        request['createdAt'] = now.strftime('%Y-%m-%d %H:%M:%S')
        request['httpProtocol'] = "HTTP/1.1"
        request['method'] = random.choice(methods)
        request['url'] = random.choice(urls)
        request['response'] = {}
        request['response']['id'] = i
        request['response']['createdAt'] = now.strftime('%Y-%m-%d %H:%M:%S')
        request['response']['httpProtocol'] = "HTTP/1.1"
        status = random.choice(statuses)
        request['response']['statusCode'] = status[0]
        request['response']['statusDescription'] = status[1]
        data['requests'].append(request)

    return JsonResponse(data)


@login_required
def session_new(request):
    step = request.GET.get('step')
    if step not in WIZARD_STEPS:
        step = '1'

    progress = int(step) * 100 / len(WIZARD_STEPS)

    args = {}
    args['progress'] = progress
    args['step'] = step

    return render(request, 'sessions/session_new.html', args)


@login_required
def session_list(request):

    url = '%s/session/' % (settings.API_BASE_URL,)
    headers = {'X-Auth-Token': request.user.password}
    r = requests.get(url, headers=headers)

    if r.status_code != requests.codes.ok:
        return signout(request)

    sessions = json.loads(r.text)

    return render(request, 'sessions/session_list.html', sessions)


@login_required
def session_details(request, id):
    url = get_mock_url('session-details.json')
    r = requests.get(url)
    session = json.loads(r.text)

    args = {}
    args['session'] = session

    return render(request, 'sessions/session_details.html', args)


@login_required
def session_execution(request, id):
    url = get_mock_url('session-details.json')
    r = requests.get(url)
    session = json.loads(r.text)

    args = {}
    args['session'] = session

    return render(request, 'sessions/session_execution.html', args)


@login_required
def session_update(request):
    if not request.POST:
        return redirect(reverse('session_list'))

    name = request.POST.get('name')
    pk = request.POST.get('pk')
    value = request.POST.get('value')

    if not name or not pk:
        response = 'field cannot be empty!'
        return HttpResponseBadRequest(response)
    else:
        # TODO: API call to update value
        return HttpResponse()


@login_required
def testplan_list(request):
    url = get_mock_url('testplan-list.json')
    r = requests.get(url)
    data = json.loads(r.text)

    args = {}
    args['data'] = data

    return render(request, 'testplan/testplan_list.html', args)


@login_required
def testplan_details(request, id):
    url = get_mock_url('testplan-details.json')
    r = requests.get(url)
    testplan = json.loads(r.text)

    args = {}
    args['testplan'] = testplan

    return render(request, 'testplan/testplan_details.html', args)


@login_required
def testplan_new(request):
    return render(request, 'testplan/testplan_new.html')


@login_required
def testplan_submit(request):
    # TODO: send APU call to save test plan
    return redirect(reverse('testplan_details', args='1'))


@login_required
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


@login_required
def execution_details(request, id):
    args = {}
    return render(request, 'execution/execution_details.html', args)


@login_required
def rule_details(request, id):
    url = get_mock_url('rule-details.json')
    r = requests.get(url)
    rule = json.loads(r.text)

    args = {}
    args['rule'] = rule

    return render(request, 'testplan/rule_details.html', args)


@login_required
def recording_list(request):
    url = get_mock_url('recording-list.json')
    r = requests.get(url)
    recordings = json.loads(r.text)

    args = {}
    args['recordings'] = recordings

    return render(request, 'recording/recording_list.html', args)


@login_required
def recording_details(request, id):
    url = get_mock_url('recording-details.json')
    r = requests.get(url)
    recording = json.loads(r.text)

    args = {}
    args['recording'] = recording

    return render(request, 'recording/recording_details.html', args)


@login_required
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


@login_required
def settings_view(request):
    return render(request, 'settings/settings.html')


def get_mock_url(file):
    static_path = static('mock/%s' % file)
    url = "%s://%s:%s%s" % (MOCK_PROTOCOL, MOCK_HOST, MOCK_PORT, static_path)
    return url
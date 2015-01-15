from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
import requests
import json
import random


MOCK_PROTOCOL = "http"
MOCK_HOST = "127.0.0.1"
MOCK_PORT = "8000"

WIZARD_STEPS = ['1', '2', '3', '4']


def signin(request):
    return render(request, 'signin.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def ajax_traffic(request):
    r = {'count': random.randint(0, 100)}
    return JsonResponse(r)


def session_new(request):

    step = request.GET.get('step')
    if step not in WIZARD_STEPS:
        step = '1'

    progress = int(step) * 100 / len(WIZARD_STEPS)

    args = {}
    args['progress'] = progress
    args['step'] = step

    return render(request, 'sessions/session_new.html', args)


def session_list(request):

    url = get_mock_url('session-list.json')
    r = requests.get(url)
    sessions = json.loads(r.text)

    args = {}
    args['sessions'] = sessions

    return render(request, 'sessions/session_list.html', args)


def session_details(request, id):
    url = get_mock_url('session-details.json')
    r = requests.get(url)
    session = json.loads(r.text)

    args = {}
    args['session'] = session

    return render(request, 'sessions/session_details.html', args)


def session_execution(request, id):
    url = get_mock_url('session-details.json')
    r = requests.get(url)
    session = json.loads(r.text)

    args = {}
    args['session'] = session

    return render(request, 'sessions/session_execution.html', args)


def session_update(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('session_list'))

    name = request.POST.get('name')
    pk = request.POST.get('pk')
    value = request.POST.get('value')

    if not name or not pk:
        response = 'field cannot be empty!'
        return HttpResponseBadRequest(response)
    else:
        # TODO: API call to update value
        return HttpResponse()


def testplan_list(request):
    url = get_mock_url('testplan-list.json')
    r = requests.get(url)
    data = json.loads(r.text)

    args = {}
    args['data'] = data

    return render(request, 'testplan/testplan_list.html', args)


def testplan_details(request, id):
    url = get_mock_url('testplan-details.json')
    r = requests.get(url)
    testplan = json.loads(r.text)

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


def execution_details(request, id):
    args = {}
    return render(request, 'execution/execution_details.html', args)


def rule_details(request, id):
    url = get_mock_url('rule-details.json')
    r = requests.get(url)
    rule = json.loads(r.text)

    args = {}
    args['rule'] = rule

    return render(request, 'testplan/rule_details.html', args)


def recording_list(request):
    url = get_mock_url('recording-list.json')
    r = requests.get(url)
    recordings = json.loads(r.text)

    args = {}
    args['recordings'] = recordings

    return render(request, 'recording/recording_list.html', args)


def recording_details(request, id):
    url = get_mock_url('recording-details.json')
    r = requests.get(url)
    recording = json.loads(r.text)

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


def settings(request):
    return render(request, 'settings/settings.html')


def get_mock_url(file):
    static_path = static('mock/%s' % file)
    url = "%s://%s:%s%s" % (MOCK_PROTOCOL, MOCK_HOST, MOCK_PORT, static_path)
    return url
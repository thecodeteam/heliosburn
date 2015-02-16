import json
import re

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.conf import settings
import requests
from webui.forms import TestPlanForm


MOCK_PROTOCOL = "http"
MOCK_HOST = "127.0.0.1"
MOCK_PORT = "8000"

WIZARD_SESSION_KEY = 'session_id'

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
        messages.error(request, 'Something went wrong. %s' % (inst,))
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
    url = '%s/traffic/' % (settings.API_BASE_URL,)
    headers = {'X-Auth-Token': request.user.password}
    r = requests.get(url, headers=headers)

    if r.status_code != requests.codes.ok:
        return signout(request)

    traffic = json.loads(r.text)

    return JsonResponse(traffic)


@login_required
def session_new(request, step):
    if step == '1' and request.POST:
        session_name = request.POST.get('name')
        session_description = request.POST.get('description')
        url = '%s/session/' % (settings.API_BASE_URL,)
        headers = {'X-Auth-Token': request.user.password}
        payload = {'name': session_name, 'description': session_description}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        if 200 >= r.status_code < 300:
            location = r.headers.get('location')
            pattern = '.+session\/(?P<id>\d+)'
            p = re.compile(pattern)
            m = p.match(location)
            try:
                session_id = m.group('id')
                request.session[WIZARD_SESSION_KEY] = session_id
                return HttpResponseRedirect(reverse('session_new', args=('2',)))
            except:
                messages.error(request, 'Could not get Session ID.')
        else:
            messages.error(request, 'Could not save the Session. Server returned: %d %s' % (r.status_code, r.text))

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
    url = '%s/testplan/' % (settings.API_BASE_URL,)
    headers = {'X-Auth-Token': request.user.password}
    r = requests.get(url, headers=headers)

    if r.status_code != requests.codes.ok:
        return signout(request)

    testplans = json.loads(r.text)

    return render(request, 'testplan/testplan_list.html', testplans)


@login_required
def testplan_details(request, id):
    url = '%s/testplan/%s' % (settings.API_BASE_URL, id)
    headers = {'X-Auth-Token': request.user.password}
    r = requests.get(url, headers=headers)

    if r.status_code == requests.codes.not_found:
        return render(request, '404.html')

    if r.status_code != requests.codes.ok:
        # TODO: do not sign out always, only if HTTP Unauthorized
        return signout(request)

    data = {'testplan': json.loads(r.text)}

    # Get Rules
    # TODO: maybe the Test Plan call should return the list of rules
    url = '%s/testplan/%s/rule' % (settings.API_BASE_URL, id)
    r = requests.get(url, headers=headers)
    if r.status_code != requests.codes.ok:
        # TODO: do not sign out always, only if HTTP Unauthorized
        return signout(request)

    data['rules'] = json.loads(r.text)

    sample_rule = {}
    sample_rule['id'] = 1
    sample_rule['type'] = "request"
    sample_rule['filter'] = "GET /cool-url/?param=wow"
    sample_rule['action'] = "GET -> POST"
    sample_rule['enabled'] = True

    data['rules']['rules'].append(sample_rule)

    return render(request, 'testplan/testplan_details.html', data)


@login_required
def testplan_new(request):

    if request.method == 'POST':
        form = TestPlanForm(request.POST)
        if form.is_valid():
            url = '%s/testplan/' % (settings.API_BASE_URL,)
            headers = {'X-Auth-Token': request.user.password}
            r = requests.post(url, headers=headers, data=json.dumps(form.cleaned_data))

            if r.status_code < 200 or r.status_code >= 300:
                return signout(request)

            # TODO: get the Test Plan ID from the Location header (when enabled in the API)
            json_body = json.loads(r.text)
            testplan_id = json_body['id']
            return HttpResponseRedirect(reverse('testplan_details', args=(str(testplan_id),)))
    else:
        form = TestPlanForm()

    return render(request, 'testplan/testplan_new.html', {'form': form})


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

    if name == 'latencyEnabled':
        value = True if value == '1' else False

    url = '%s/testplan/%s' % (settings.API_BASE_URL, pk)
    headers = {'X-Auth-Token': request.user.password}
    data = {name: value}
    r = requests.put(url, headers=headers, data=json.dumps(data))
    if r.status_code != requests.codes.ok:
        return HttpResponse(status=r.status_code, content='Error updating the Test Plan. %s' % (r.text,))
    return HttpResponse()


@login_required
def testplan_delete(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('testplan_list'))

    headers = {'X-Auth-Token': request.user.password}
    testplans = request.POST.getlist('testplans[]')

    # Workaround to support different kinds of form submission
    if testplans is None or len(testplans) == 0:
        testplans = request.POST.getlist('testplans')
        
    for testplan_id in testplans:
        url = '%s/testplan/%s' % (settings.API_BASE_URL, testplan_id)
        r = requests.delete(url, headers=headers)
        if r.status_code != requests.codes.ok:
            return HttpResponse(status=r.status_code, content='Error deleting the Test Plan. %s' % (r.text,))
    return HttpResponse()


@login_required
def execution_details(request, id):
    args = {}
    return render(request, 'execution/execution_details.html', args)


@login_required
def rule_details(request, testplan_id, rule_id):
    url = '%s/testplan/%s' % (settings.API_BASE_URL, testplan_id)
    headers = {'X-Auth-Token': request.user.password}
    r = requests.get(url, headers=headers)

    if r.status_code == requests.codes.not_found:
        return render(request, '404.html')

    if r.status_code != requests.codes.ok:
        # TODO: do not sign out always, only if HTTP Unauthorized
        return signout(request)

    data = {'testplan': json.loads(r.text)}

    url = get_mock_url('rule-details.json')
    r = requests.get(url)
    rule = json.loads(r.text)
    data['rule'] = rule

    return render(request, 'testplan/rule_details.html', data)


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
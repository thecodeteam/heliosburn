import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
import requests
from webui.views import signout, get_mock_url


WIZARD_SESSION_KEY = 'session_id'
WIZARD_STEPS = ['1', '2', '3', '4']

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
            session_id = get_resource_id_from_header('session', r)
            if session_id:
                request.session[WIZARD_SESSION_KEY] = session_id
                return HttpResponseRedirect(reverse('session_new', args=(str(session_id),)))
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

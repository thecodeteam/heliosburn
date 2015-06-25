import logging
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
import requests

from webui.exceptions import UnauthorizedException
from webui.models import Session
from webui.views import signout, get_mock_url


logger = logging.getLogger(__name__)

@login_required
def session_new(request):
    return render(request, 'sessions/session_new.html')


@login_required
def session_create(request):
    data = json.loads(request.body)

    try:
        session_id = Session(auth_token=request.user.password).create(data)
    except UnauthorizedException:
        logger.warning('User unauthorized. Signing out...')
        return signout(request)
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        return render(request, '500.html', {'message': inst.message})

    url = reverse('session_details', args=(session_id,))
    return HttpResponse(url)


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

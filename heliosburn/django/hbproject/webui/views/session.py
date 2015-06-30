import logging
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import requests

from webui.exceptions import UnauthorizedException, NotFoundException, ServerErrorException
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
def session_details(request, session_id):
    try:
        session = Session(auth_token=request.user.password).get(session_id)
    except UnauthorizedException:
        logger.warning('User unauthorized. Signing out...')
        return signout(request)
    except NotFoundException:
        logger.warning('The requested Session "%s" does not exist', session_id)
        return render(request, '404.html')
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        messages.error(request, inst.message if inst.message else 'Unexpected error')
        return HttpResponseRedirect(reverse('session_list'))

    data = {'session': session}
    return render(request, 'sessions/session_details.html', data)


@login_required
def session_execute(request, session_id):

    try:
        session = Session(auth_token=request.user.password).get(session_id)
        data = {'session': session}
        return render(request, 'sessions/session_execution.html', data)
    except UnauthorizedException:
        logger.warning('User unauthorized. Signing out...')
        return signout(request)
    except NotFoundException:
        logger.warning('The requested Session "%s" does not exist', session_id)
        return render(request, '404.html')
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        messages.error(request, inst.message if inst.message else 'Unexpected error')
        return HttpResponseRedirect(reverse('session_details', args=(str(session_id),)))


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
@csrf_exempt
def session_start(request, session_id):
    if request.method != 'POST':
        return HttpResponseBadRequest('Method must be POST')

    try:
        Session(auth_token=request.user.password).start(session_id)
    except UnauthorizedException:
        logger.warning('User unauthorized. Signing out...')
        signout(request)
        return HttpResponseBadRequest('Unauthorized')
    except NotFoundException:
        logger.warning('The requested Session "%s" does not exist', session_id)
        return HttpResponseBadRequest('Resource not found')
    except ServerErrorException:
        logger.error('Unexpected exception in the API', exc_info=True)
        return HttpResponseServerError()
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        message = inst.message if inst.message else 'Unexpected error'
        return HttpResponseBadRequest(message)
    return HttpResponse('started')


@login_required
@csrf_exempt
def session_stop(request, session_id):
    if request.method != 'POST':
        return HttpResponseBadRequest('Method must be POST')

    try:
        Session(auth_token=request.user.password).stop(session_id)
    except UnauthorizedException:
        logger.warning('User unauthorized. Signing out...')
        signout(request)
        return HttpResponseBadRequest('Unauthorized')
    except NotFoundException:
        logger.warning('The requested Session "%s" does not exist', session_id)
        return HttpResponseBadRequest('Resource not found')
    except ServerErrorException:
        logger.error('Unexpected exception in the API', exc_info=True)
        return HttpResponseServerError()
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        message = inst.message if inst.message else 'Unexpected error'
        return HttpResponseBadRequest(message)

    return HttpResponse('stopped')
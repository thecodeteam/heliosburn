from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from webui.exceptions import UnauthorizedException, NotFoundException, ServerErrorException
from webui.forms import RecordingForm
from webui.models import Recording
from webui.views import signout


@login_required
def recording_list(request):
    try:
        recordings = Recording(auth_token=request.user.password).get_all()
    except UnauthorizedException:
        return signout(request)
    except Exception as inst:
        return render(request, '500.html', {'message': inst.message})

    form = RecordingForm()
    data = dict()
    data['recordings'] = recordings['recordings']
    data['form'] = form
    return render(request, 'recording/recording_list.html', data)


@login_required
def recording_new(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('recording_list'))

    form = RecordingForm(request.POST)
    if form.is_valid():
        try:
            recording_id = Recording(auth_token=request.user.password).create(form.cleaned_data)
            messages.success(request, 'Recording created successfully')
            return HttpResponseRedirect(reverse('recording_live', args=(str(recording_id),)))
        except UnauthorizedException:
            return signout(request)
        except NotFoundException:
            return render(request, '404.html')
        except Exception as inst:
            messages.error(request, inst.message if inst.message else 'Unexpected error')
            return HttpResponseRedirect(reverse('recording_list'))
    messages.error(request, 'Could not create the recording. Invalid fields.')
    return HttpResponseRedirect(reverse('recording_list'))


@login_required
def recording_details(request, recording_id):
    try:
        recording = Recording(auth_token=request.user.password).get(recording_id)
    except UnauthorizedException:
        return signout(request)
    except NotFoundException:
        return render(request, '404.html')
    except Exception as inst:
        messages.error(request, inst.message if inst.message else 'Unexpected error')
        return HttpResponseRedirect(reverse('recording_list'))

    if 'startedAt' not in recording:
        return HttpResponseRedirect(reverse('recording_live', args=(str(recording_id),)))

    data = {'recording': recording}
    return render(request, 'recording/recording_details.html', data)


@login_required
def recording_live(request, recording_id):
    try:
        recording = Recording(auth_token=request.user.password).get(recording_id)
    except UnauthorizedException:
        return signout(request)
    except NotFoundException:
        return render(request, '404.html')
    except Exception as inst:
        messages.error(request, inst.message if inst.message else 'Unexpected error')
        return HttpResponseRedirect(reverse('recording_list'))

    if 'startedAt' and 'stoppedAt' in recording:
        return HttpResponseRedirect(reverse('recording_details', args=(str(recording_id),)))

    data = {'recording': recording}
    return render(request, 'recording/recording_live.html', data)


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

    try:
        Recording(auth_token=request.user.password).update(pk, {name: value})
    except Exception as inst:
        return HttpResponseBadRequest(content='Error updating the recording. {}'.format(inst.message))
    return HttpResponse()


@login_required
@csrf_exempt
def recording_start(request, recording_id):
    if request.method != 'POST':
        return HttpResponseBadRequest('Method must be POST')

    try:
        info = Recording(auth_token=request.user.password).start(recording_id)
    except UnauthorizedException:
        signout(request)
        return HttpResponseBadRequest('Unauthorized')
    except NotFoundException:
        return HttpResponseBadRequest('Resource not found')
    except ServerErrorException:
        return HttpResponseServerError()
    except Exception as inst:
        message = inst.message if inst.message else 'Unexpected error'
        return HttpResponseBadRequest(message)
    return HttpResponse('started')


@login_required
@csrf_exempt
def recording_stop(request, recording_id):
    if request.method != 'POST':
        return HttpResponseBadRequest('Method must be POST')

    try:
        info = Recording(auth_token=request.user.password).stop(recording_id)
    except UnauthorizedException:
        signout(request)
        return HttpResponseBadRequest('Unauthorized')
    except NotFoundException:
        return HttpResponseBadRequest('Resource not found')
    except ServerErrorException:
        return HttpResponseServerError()
    except Exception as inst:
        message = inst.message if inst.message else 'Unexpected error'
        return HttpResponseBadRequest(message)

    return HttpResponse('stopped')
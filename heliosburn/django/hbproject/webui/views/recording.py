import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
import requests
from webui.exceptions import UnauthorizedException, NotFoundException
from webui.forms import RecordingForm
from webui.models import Recording
from webui.views import get_mock_url, signout


@login_required
def recording_list(request):
    try:
        recordings = Recording(auth_token=request.user.password).get_all()
    except UnauthorizedException:
        return signout(request)
    except Exception as inst:
        return render(request, '500.html', {'message': inst.message})

    return render(request, 'recording/recording_list.html', recordings)


@login_required
def recording_new(request):
    form = RecordingForm(request.POST or None)
    if form.is_valid():
        try:
            recording_id = Recording(auth_token=request.user.password).create(form.cleaned_data)
            messages.success(request, 'Recording created successfully')
            return HttpResponseRedirect(reverse('recording_details', args=(str(recording_id),)))
        except UnauthorizedException:
            return signout(request)
        except NotFoundException:
            return render(request, '404.html')
        except Exception as inst:
            messages.error(request, inst.message if inst.message else 'Unexpected error')
            return HttpResponseRedirect(reverse('recording_list'))
    return render(request, 'recording/recording_new.html', {'form': form})


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
        return HttpResponseRedirect(reverse('testplan_list'))

    data = {'recording': recording}
    return render(request, 'recording/recording_details.html', data)


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
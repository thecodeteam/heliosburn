import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
import requests
from webui.views import get_mock_url


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
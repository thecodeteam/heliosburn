import json
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.staticfiles.templatetags.staticfiles import static
import requests


MOCK_PROTOCOL = "http"
MOCK_HOST = "127.0.0.1"
MOCK_PORT = "8000"


def signout(request):
    auth.logout(request)
    return redirect(reverse('signin'))


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
def execution_details(request, id):
    args = {}
    return render(request, 'execution/execution_details.html', args)


@login_required
def settings_view(request):
    return render(request, 'settings/settings.html')


def get_mock_url(file):
    static_path = static('mock/%s' % file)
    url = "%s://%s:%s%s" % (MOCK_PROTOCOL, MOCK_HOST, MOCK_PORT, static_path)
    return url
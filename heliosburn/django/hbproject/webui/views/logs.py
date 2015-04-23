import logging

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import View

from webui.exceptions import UnauthorizedException
from webui.models import Logs
from webui.views import signout


logger = logging.getLogger(__name__)


class LogsView(View):
    template_name = 'logs/logs.html'

    def get(self, request):

        if 'application/json' in request.META.get('HTTP_ACCEPT'):
            return self._handle_ajax(request)

        try:
            stats = Logs(auth_token=request.user.password).stats()
        except UnauthorizedException:
            logger.warning('User unauthorized. Signing out...')
            return signout(request)
        except Exception as inst:
            logger.error('Unexpected exception', exc_info=True)
            messages.error(request, inst.message if inst.message else 'Unexpected error')
            return HttpResponseRedirect(reverse('dashboard'))

        data = dict()
        data['stats'] = stats

        return render(request, self.template_name, data)

    def _handle_ajax(self, request):

        start = request.GET.get('start', '0')
        length = request.GET.get('length', '10')
        component = request.GET.get('component', '')
        levels = request.GET.get('levels', '')
        date = request.GET.get('date', '').split(' - ')
        if len(date) == 2:
            date_from, date_to = date[0], date[1]
        else:
            date_from = date_to = ''
        msg = request.GET.get('msg', '')

        try:
            logs = Logs(auth_token=request.user.password).get(start, length, component, levels,
                                                              date_from, date_to, msg)
        except Exception as inst:
            return HttpResponseBadRequest(inst)

        data = dict()
        data['recordsTotal'] = logs['matchedEntries']
        data['recordsFiltered'] = logs['matchedEntries']
        data['data'] = []
        for entry in logs['log']:
            log_entry = [entry['time'], entry['name'], entry['level'], entry['msg']]
            data['data'].append(log_entry)
        return JsonResponse(data)
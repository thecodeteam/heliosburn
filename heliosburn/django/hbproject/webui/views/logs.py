import logging
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.views.generic import View
from webui.exceptions import UnauthorizedException
from webui.models import Logs
from webui.views import signout


logger = logging.getLogger(__name__)


class LogsView(View):
    template_name = 'logs/logs.html'

    def get(self, request):
        try:
            stats = Logs(auth_token=request.user.password).stats()
            logs = Logs(auth_token=request.user.password).get()
        except UnauthorizedException:
            logger.warning('User unauthorized. Signing out...')
            return signout(request)
        except Exception as inst:
            logger.error('Unexpected exception', exc_info=True)
            messages.error(request, inst.message if inst.message else 'Unexpected error')
            return HttpResponseRedirect(reverse('dashboard'))

        data = dict()
        data['stats'] = stats
        data['logs'] = logs

        return render(request, self.template_name, data)
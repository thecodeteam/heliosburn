import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

logger = logging.getLogger(__name__)


class DashboardView(View):
    template_name = 'dashboard.html'

    @method_decorator(login_required)
    def get(self, request):
        args = {'maxRequests': 20}
        return render(request, self.template_name, args)
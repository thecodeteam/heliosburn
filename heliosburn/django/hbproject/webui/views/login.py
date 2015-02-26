from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from webui.forms import LoginForm
from django.contrib import auth, messages


class LoginView(View):
    form_class = LoginForm
    template_name = 'signin.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        try:
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        except Exception as inst:
            messages.error(request, 'Something went wrong. %s' % (inst,))
            return render(request, self.template_name, {'form': form})

        if not user:
            messages.error(request, 'Invalid login credentials')
            return render(request, self.template_name, {'form': form})

        auth.login(request, user)
        redirect_url = request.GET.get('next', reverse('dashboard'))
        return HttpResponseRedirect(redirect_url)
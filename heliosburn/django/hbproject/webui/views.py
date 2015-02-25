import json

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import View
import requests
from webui.forms import TestPlanForm, RuleRequestForm, RuleForm, LoginForm
from webui.models import TestPlan, Rule
from webui.exceptions import UnauthorizedException, NotFoundException, BadRequestException


WIZARD_SESSION_KEY = 'session_id'
WIZARD_STEPS = ['1', '2', '3', '4']


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


def signout(request):
    auth.logout(request)
    return redirect(reverse('signin'))


class DashboardView(View):
    template_name = 'dashboard.html'

    @method_decorator(login_required)
    def get(self, request):
        args = {'maxRequests': 20}
        return render(request, self.template_name, args)


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
def session_new(request, step):
    if step == '1' and request.POST:
        session_name = request.POST.get('name')
        session_description = request.POST.get('description')
        url = '%s/session/' % (settings.API_BASE_URL,)
        headers = {'X-Auth-Token': request.user.password}
        payload = {'name': session_name, 'description': session_description}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        if 200 >= r.status_code < 300:
            session_id = get_resource_id_from_header('session', r)
            if session_id:
                request.session[WIZARD_SESSION_KEY] = session_id
                return HttpResponseRedirect(reverse('session_new', args=(str(session_id),)))
            messages.error(request, 'Could not get Session ID.')
        else:
            messages.error(request, 'Could not save the Session. Server returned: %d %s' % (r.status_code, r.text))

    progress = int(step) * 100 / len(WIZARD_STEPS)

    args = {}
    args['progress'] = progress
    args['step'] = step

    return render(request, 'sessions/session_new.html', args)


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


@login_required
def testplan_list(request):
    try:
        testplans = TestPlan(auth_token=request.user.password).get_all()
    except UnauthorizedException:
        return signout(request)
    except Exception as inst:
        return render(request, '500.html', {'message': inst.message})

    return render(request, 'testplan/testplan_list.html', testplans)


@login_required
def testplan_details(request, testplan_id):
    try:
        testplan = TestPlan(auth_token=request.user.password).get(testplan_id)
        # TODO: the Test Plan call should return the list of rules
        # rules = Rule(testplan_id, auth_token=request.user.password).get_all()
        rules = {'rules': []}  # TODO: remove it once API Rule's endpoint is fixed
    except UnauthorizedException:
        return signout(request)
    except NotFoundException:
        return render(request, '404.html')
    except Exception as inst:
        messages.error(request, inst.message if inst.message else 'Unexpected error')
        return HttpResponseRedirect(reverse('testplan_list'))

    data = {'testplan': testplan, 'rules': rules}
    return render(request, 'testplan/testplan_details.html', data)


@login_required
def testplan_new(request):
    form = TestPlanForm(request.POST or None)
    if form.is_valid():
        try:
            testplan_id = TestPlan(auth_token=request.user.password).create(form.cleaned_data)
            return HttpResponseRedirect(reverse('testplan_details', args=(str(testplan_id),)))
        except UnauthorizedException:
            return signout(request)
        except NotFoundException:
            return render(request, '404.html')
        except Exception as inst:
            messages.error(request, inst.message if inst.message else 'Unexpected error')
            return HttpResponseRedirect(reverse('testplan_list'))

    return render(request, 'testplan/testplan_new.html', {'form': form})


@login_required
def testplan_update(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('testplan_list'))

    name = request.POST.get('name')
    pk = request.POST.get('pk')
    value = request.POST.get('value')

    if not name or not pk:
        response = 'field cannot be empty!'
        return HttpResponseBadRequest(response)

    if name == 'latencyEnabled':
        value = True if value == '1' else False

    try:
        TestPlan(auth_token=request.user.password).update(pk, {name: value})
    except Exception as inst:
        return HttpResponseBadRequest(content='Error updating the Test Plan. {}'.format(inst.message))
    return HttpResponse()


@login_required
def testplan_delete(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('testplan_list'))

    testplans = request.POST.getlist('testplans[]')
    # Workaround to support different kinds of form submission
    if testplans is None or len(testplans) == 0:
        testplans = request.POST.getlist('testplans')

    t = TestPlan(auth_token=request.user.password)
    for testplan_id in testplans:
        try:
            t.delete(testplan_id)
        except NotFoundException:
            return HttpResponseNotFound()
        except Exception as inst:
            return HttpResponseBadRequest()
    return HttpResponse()


@login_required
def execution_details(request, id):
    args = {}
    return render(request, 'execution/execution_details.html', args)


@login_required
def rule_details(request, testplan_id, rule_id):
    try:
        testplan = TestPlan(auth_token=request.user.password).get(testplan_id)
        rule = Rule(testplan_id, auth_token=request.user.password).get(rule_id)
        # check if the Rule belongs to the Test Plan
        if str(rule['testPlanId']) != testplan_id:
            return render(request, '404.html')
    except UnauthorizedException:
        return signout(request)
    except NotFoundException:
        return render(request, '404.html')
    except Exception as inst:
        messages.error(request, inst.message if inst.message else 'Unexpected error')
        return HttpResponseRedirect(reverse('testplan_list'))

    data = {'testplan': testplan, 'rule': rule, 'form': RuleRequestForm()}
    return render(request, 'rules/rule_details.html', data)


@login_required
def rule_new(request, testplan_id):
    form = RuleForm(request.POST or None)

    if form.is_valid():
        url = '%s/testplan/%s/rule' % (settings.API_BASE_URL, str(testplan_id))
        headers = {'X-Auth-Token': request.user.password}
        r = requests.post(url, headers=headers, data=json.dumps(form.cleaned_data))
        if r.status_code < 200 or r.status_code >= 300:
            return signout(request)

        rule_id = get_resource_id_from_header('rule', r)
        if rule_id:
            return HttpResponseRedirect(reverse('rule_details', args=(str(testplan_id), str(rule_id))))
        else:
            messages.warning(request, 'Rule was created successfully, but we could not retrieve its ID')
            return HttpResponseRedirect(reverse('testplan_details', args=(str(testplan_id),)))

    url = '%s/testplan/%s' % (settings.API_BASE_URL, testplan_id)
    headers = {'X-Auth-Token': request.user.password}
    r = requests.get(url, headers=headers)

    if r.status_code == requests.codes.not_found:
        return render(request, '404.html')

    if r.status_code != requests.codes.ok:
        # TODO: do not sign out always, only if HTTP Unauthorized
        return signout(request)

    data = {}
    data['testplan'] = json.loads(r.text)
    data['form'] = form

    return render(request, 'rules/rule_new.html', data)


@login_required
def rule_update(request, testplan_id, rule_id):
    return HttpResponse()


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


@login_required
def settings_view(request):
    return render(request, 'settings/settings.html')


def get_mock_url(file):
    static_path = static('mock/%s' % file)
    url = "%s://%s:%s%s" % (MOCK_PROTOCOL, MOCK_HOST, MOCK_PORT, static_path)
    return url
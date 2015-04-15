import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from webui.exceptions import UnauthorizedException, NotFoundException
from webui.forms import TestPlanForm
from webui.models import TestPlan
from webui.views import signout

logger = logging.getLogger(__name__)


@login_required
def testplan_list(request):
    try:
        testplans = TestPlan(auth_token=request.user.password).get_all()
    except UnauthorizedException:
        logger.warning('User unauthorized. Signing out...')
        return signout(request)
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        return render(request, '500.html', {'message': inst.message})

    return render(request, 'testplan/testplan_list.html', testplans)


@login_required
def testplan_details(request, testplan_id):
    try:
        testplan = TestPlan(auth_token=request.user.password).get(testplan_id)
        # rules = Rule(testplan_id, auth_token=request.user.password).get_all()
    except UnauthorizedException:
        logger.warning('User unauthorized. Signing out...')
        return signout(request)
    except NotFoundException:
        logger.warning('The requested Test Plan "%s" does not exist', testplan_id)
        return render(request, '404.html')
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        messages.error(request, inst.message if inst.message else 'Unexpected error')
        return HttpResponseRedirect(reverse('testplan_list'))

    data = {'testplan': testplan}
    return render(request, 'testplan/testplan_details.html', data)


@login_required
def testplan_new(request):
    form = TestPlanForm(request.POST or None)
    if form.is_valid():
        try:
            testplan_id = TestPlan(auth_token=request.user.password).create(form.cleaned_data)
            return HttpResponseRedirect(reverse('testplan_details', args=(str(testplan_id),)))
        except UnauthorizedException:
            logger.warning('User unauthorized. Signing out...')
            return signout(request)
        except Exception as inst:
            logger.error('Unexpected exception', exc_info=True)
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
    elif name == 'clientLatency' or name == 'serverLatency':
        value = int(value)

    try:
        TestPlan(auth_token=request.user.password).update(pk, {name: value})
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
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
            logger.warning('The requested Test Plan "%s" does not exist', testplan_id)
            return HttpResponseNotFound()
        except Exception as inst:
            logger.error('Unexpected exception', exc_info=True)
            return HttpResponseBadRequest()
    return HttpResponse()

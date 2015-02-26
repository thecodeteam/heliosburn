from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from webui.exceptions import UnauthorizedException, NotFoundException
from webui.forms import RuleRequestForm, RuleForm
from webui.models import TestPlan, Rule
from webui.views import signout


@login_required
def rule_details(request, testplan_id, rule_id):
    try:
        testplan = TestPlan(auth_token=request.user.password).get(testplan_id)
        rule = Rule(testplan_id, auth_token=request.user.password).get(rule_id)
        # check if the Rule belongs to the Test Plan
        # FIXME: API should return the "testplanId" within the Rule
        # if str(rule['testPlanId']) != testplan_id:
        #     return render(request, '404.html')
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
    try:
        testplan = TestPlan(auth_token=request.user.password).get(testplan_id)
    except UnauthorizedException:
        return signout(request)
    except NotFoundException:
        return render(request, '404.html')
    except Exception as inst:
        messages.error(request, inst.message if inst.message else 'Unexpected error')
        return HttpResponseRedirect(reverse('testplan_list'))

    form = RuleForm(request.POST or None)
    if form.is_valid():
        try:
            rule_id = Rule(testplan_id, auth_token=request.user.password).create(form.cleaned_data)
            return HttpResponseRedirect(reverse('rule_details', args=(str(testplan_id), str(rule_id))))
        except UnauthorizedException:
            return signout(request)
        except Exception as inst:
            messages.error(request, inst.message if inst.message else 'Unexpected error')
            return HttpResponseRedirect(reverse('rule_new', args=(str(testplan_id),)))

    return render(request, 'rules/rule_new.html', {'form': form, 'testplan': testplan})


@login_required
def rule_update(request, testplan_id, rule_id):
    if not request.POST:
        return HttpResponseRedirect(reverse('rule_details', args=(str(testplan_id), str(rule_id))))

    name = request.POST.get('name')
    pk = request.POST.get('pk')
    value = request.POST.get('value')

    if not name or not pk:
        response = 'field cannot be empty!'
        return HttpResponseBadRequest(response)

    try:
        Rule(testplan_id, auth_token=request.user.password).update(pk, {name: value})
    except Exception as inst:
        return HttpResponseBadRequest(content='Error updating the Test Plan. {}'.format(inst.message))
    return HttpResponse()
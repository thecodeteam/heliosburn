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

    initial_data = _rule_to_post_data(rule)

    form = RuleRequestForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        try:
            Rule(testplan_id, auth_token=request.user.password).update(rule['id'], form.cleaned_data)
            messages.success(request, "The rule was updated successfully.")
            return HttpResponseRedirect(reverse('rule_details', args=(str(testplan_id), str(rule_id))))
        except UnauthorizedException:
            return signout(request)
        except Exception as inst:
            messages.error(request, inst.message if inst.message else 'Unexpected error')
            return HttpResponseRedirect(reverse('rule_details', args=(str(testplan_id), str(rule_id))))

    data = {'testplan': testplan, 'rule': rule, 'form': form}
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

    if name == 'enabled':
        value = False if value == '0' else True

    try:
        Rule(testplan_id, auth_token=request.user.password).update(pk, {name: value})
    except Exception as inst:
        return HttpResponseBadRequest(content='Error updating the Test Plan. {}'.format(inst.message))
    return HttpResponse()


def _rule_to_post_data(rule):
    post_data = {}
    post_data['ruleType'] = rule['ruleType']

    if 'filter' in rule:
        filter = rule['filter']
        if 'httpProtocol' in filter:
            post_data['filterProtocol'] = filter['httpProtocol']
        if 'method' in filter:
            post_data['filterMethod'] = filter['method']
        if 'url' in filter:
            post_data['filterUrl'] = filter['url']
        if 'statusCode' in filter:
            post_data['filterstatusCode'] = filter['statusCode']

    if 'action' in rule:
        action = rule['action']
        if 'type' in action:
            post_data['actionType'] = action['type']
        if 'httpProtocol' in action:
            post_data['actionProtocol'] = action['httpProtocol']
        if 'method' in action:
            post_data['actionMethod'] = action['method']
        if 'url' in action:
            post_data['actionUrl'] = action['url']
        if 'statusCode' in action:
            post_data['actionStatusCode'] = action['statusCode']
        if 'statusDescription' in action:
            post_data['actionStatusDescription'] = action['statusDescription']
        if 'payload' in action:
            post_data['actionPayload'] = action['payload']
        if 'setHeaders' in action:
            action['headers'] = action.pop('setHeaders')
    return post_data

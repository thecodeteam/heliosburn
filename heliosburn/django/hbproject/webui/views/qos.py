import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from webui.exceptions import UnauthorizedException, NotFoundException
from webui.forms import TestPlanForm, QoSForm
from webui.models import QoS
from webui.views import signout

logger = logging.getLogger(__name__)


@login_required
def qos_list(request):

    try:
        qoss = QoS(auth_token=request.user.password).get_all()
    except UnauthorizedException:
        logger.warning('User unauthorized. Signing out...')
        return signout(request)
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        return render(request, '500.html', {'message': inst.message})

    if request.is_ajax():
        return JsonResponse(qoss)

    return render(request, 'qos/qos_list.html', qoss)


@login_required
def qos_details(request, qos_id):
    try:
        qos = QoS(auth_token=request.user.password).get(qos_id)
    except UnauthorizedException:
        logger.warning('User unauthorized. Signing out...')
        return signout(request)
    except NotFoundException:
        logger.warning('The requested Test Plan "%s" does not exist', qos_id)
        return render(request, '404.html')
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        messages.error(request, inst.message if inst.message else 'Unexpected error')
        return HttpResponseRedirect(reverse('qos_list'))

    data = {'qos': qos}
    return render(request, 'qos/qos_details.html', data)


@login_required
def qos_new(request):
    form = QoSForm(request.POST or None)
    if form.is_valid():
        try:
            qos_id = QoS(auth_token=request.user.password).create(form.cleaned_data)
            return HttpResponseRedirect(reverse('qos_details', args=(str(qos_id),)))
        except UnauthorizedException:
            logger.warning('User unauthorized. Signing out...')
            return signout(request)
        except Exception as inst:
            logger.error('Unexpected exception', exc_info=True)
            messages.error(request, inst.message if inst.message else 'Unexpected error')
            return HttpResponseRedirect(reverse('qos_list'))

    return render(request, 'qos/qos_new.html', {'form': form})


@login_required
def qos_update(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('qos_list'))

    name = request.POST.get('name')
    pk = request.POST.get('pk')
    value = request.POST.get('value')

    if not name or not pk:
        response = 'field cannot be empty!'
        return HttpResponseBadRequest(response)

    if name == 'jitter-min':
        name = 'jitter'
        value = {'min': value}
    elif name == 'jitter-max':
        name = 'jitter'
        value = {'max': value}

    try:
        QoS(auth_token=request.user.password).update(pk, {name: value})
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        return HttpResponseBadRequest(content='Error updating the Test Plan. {}'.format(inst.message))
    return HttpResponse()


@login_required
def qos_delete(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('qos_list'))

    qoss = request.POST.getlist('qos[]')
    # Workaround to support different kinds of form submission
    if qoss is None or len(qoss) == 0:
        qoss = request.POST.getlist('qos')

    t = QoS(auth_token=request.user.password)
    for qos_id in qoss:
        try:
            t.delete(qos_id)
        except NotFoundException:
            logger.warning('The requested Test Plan "%s" does not exist', qos_id)
            return HttpResponseNotFound()
        except Exception as inst:
            logger.error('Unexpected exception', exc_info=True)
            return HttpResponseBadRequest()
    return HttpResponse()

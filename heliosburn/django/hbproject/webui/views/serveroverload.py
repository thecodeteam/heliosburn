import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from webui.exceptions import UnauthorizedException, NotFoundException
from webui.forms import ServerOverloadForm
from webui.models import ServerOverload
from webui.views import signout

logger = logging.getLogger(__name__)


@login_required
def serveroverload_list(request):

    try:
        serveroverloads = ServerOverload(auth_token=request.user.password).get_all()
    except UnauthorizedException:
        logger.warning('User unauthorized. Signing out...')
        return signout(request)
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        return render(request, '500.html', {'message': inst.message})

    if request.is_ajax():
        return JsonResponse(serveroverloads)

    return render(request, 'serveroverload/serveroverload_list.html', serveroverloads)


@login_required
def serveroverload_details(request, serveroverload_id):
    try:
        serveroverload = ServerOverload(auth_token=request.user.password).get(serveroverload_id)
    except UnauthorizedException:
        logger.warning('User unauthorized. Signing out...')
        return signout(request)
    except NotFoundException:
        logger.warning('The requested Server Overload profile "%s" does not exist', serveroverload_id)
        return render(request, '404.html')
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        messages.error(request, inst.message if inst.message else 'Unexpected error')
        return HttpResponseRedirect(reverse('serveroverload_list'))

    data = {'serveroverload': serveroverload}
    return render(request, 'serveroverload/serveroverload_details.html', data)


@login_required
def serveroverload_new(request):
    form = ServerOverloadForm(request.POST or None)
    if form.is_valid():
        try:
            serveroverload_id = ServerOverload(auth_token=request.user.password).create(form.cleaned_data)
            return HttpResponseRedirect(reverse('serveroverload_details', args=(str(serveroverload_id),)))
        except UnauthorizedException:
            logger.warning('User unauthorized. Signing out...')
            return signout(request)
        except Exception as inst:
            logger.error('Unexpected exception', exc_info=True)
            messages.error(request, inst.message if inst.message else 'Unexpected error')
            return HttpResponseRedirect(reverse('serveroverload_list'))

    return render(request, 'serveroverload/serveroverload_new.html', {'form': form})


@login_required
def serveroverload_update(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('serveroverload_list'))

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
        ServerOverload(auth_token=request.user.password).update(pk, {name: value})
    except Exception as inst:
        logger.error('Unexpected exception', exc_info=True)
        return HttpResponseBadRequest(content='Error updating the Server Overload profile. {}'.format(inst.message))
    return HttpResponse()


@login_required
def serveroverload_delete(request):
    if not request.POST:
        return HttpResponseRedirect(reverse('serveroverload_list'))

    serveroverloads = request.POST.getlist('serveroverload[]')
    # Workaround to support different kinds of form submission
    if serveroverloads is None or len(serveroverloads) == 0:
        serveroverloads = request.POST.getlist('serveroverload')

    t = ServerOverload(auth_token=request.user.password)
    for serveroverload_id in serveroverloads:
        try:
            t.delete(serveroverload_id)
        except NotFoundException:
            logger.warning('The requested Server Overload profile "%s" does not exist', serveroverload_id)
            return HttpResponseNotFound()
        except Exception as inst:
            logger.error('Unexpected exception', exc_info=True)
            return HttpResponseBadRequest()
    return HttpResponse()

# Views which do not belong to any specific module

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import sessions


def index(request):
    return HttpResponse("This endpoint is the Helios Burn API.")


def version(request):
    return JsonResponse({"version": "TODO"})


def test(request):  # Adrian, please take a look at this example using mongoengine
    if 'foo' in request.session:
        return HttpResponse("I've seen you before!")
    else:
        request.session['foo'] = 'bar'
        return HttpResponse("This is the first time I've seen you...")
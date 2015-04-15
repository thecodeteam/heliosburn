# Views which do not belong to any specific module

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import sessions


def index(request):
    return HttpResponse("This endpoint is the Helios Burn API.")


def version(request):
    return JsonResponse({"version": "TODO"})

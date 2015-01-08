from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api import models
import pdb

@csrf_exempt
def rest(request):
    pdb.set_trace()
    if request.method == 'GET':
        return get(request, **request.GET)
    elif request.method == 'POST':
        return post(request, **request.GET)
    elif request.method == 'PUT':
        return put(request, **request.GET)
    elif request.method == 'DELETE':
        return delete(request, **request.GET)
    else:
        return JsonResponse({"error": "HTTP METHOD UNKNOWN"})

def get(request, username):
    return JsonResponse({"method": request.method})

def post(request):
    return JsonResponse({"method": request.method})

def put(request):
    return JsonResponse({"method": request.method})

def delete(request):
    return JsonResponse({"method": request.method})

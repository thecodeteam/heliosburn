from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api import models
from IPython.core.debugger import Tracer

@csrf_exempt
def rest(request):
    Tracer()()
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

def get(request):
    return JsonResponse({__name__: request.method})

def post(request):
    return JsonResponse({__name__: request.method})

def put(request):
    return JsonResponse({__name__: request.method})

def delete(request):
    return JsonResponse({__name__: request.method})

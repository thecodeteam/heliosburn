import json

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.models.auth import RequireLogin
from api.models import redis_wrapper


@csrf_exempt
def rest(request, *pargs):
    """
    Calls python function corresponding with HTTP METHOD name. 
    Calls with incomplete arguments will return HTTP 400
    """
    if request.method == 'GET':
        rest_function = get
    elif request.method == 'POST':
        rest_function = post
    elif request.method == 'PUT':
        rest_function = put
    elif request.method == 'DELETE':
        rest_function = delete
    else:
        return JsonResponse({"error": "HTTP METHOD UNKNOWN"})

    try:
        return rest_function(request, *pargs)
    except TypeError as e:
            print e
            return HttpResponseBadRequest("unknown method")


@RequireLogin
def get(request):
    r = redis_wrapper.init_redis(0)
    traffic = r.zrangebyscore('heliosburn.traffic', '-inf', '+inf', withscores=False)
    traffic = [json.loads(traf) for traf in traffic]
    r = {
        "count": len(traffic),
        "more": False,
        "requests": traffic
        }
    return JsonResponse(r)

@RequireLogin
def post(request):
    r = HttpResponse('Invalid method. Only GET method accepted.', status=405)
    r['Allow'] = 'GET'
    return r

@RequireLogin
def put(request):
    r = HttpResponse('Invalid method. Only GET method accepted.', status=405)
    r['Allow'] = 'GET'
    return r
        

@RequireLogin
def delete(request):
    r = HttpResponse('Invalid method. Only GET method accepted.', status=405)
    r['Allow'] = 'GET'
    return r


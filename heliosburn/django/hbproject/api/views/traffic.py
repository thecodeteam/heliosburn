from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy.exc import IntegrityError
from api.models import db_model
from api.models.auth import RequireLogin
from api.models import redis_wrapper
import hashlib
import json


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
    if "from" in request.GET:
        t_from = int(request.GET['from'])
    else:
        t_from = None
    if "to" in request.GET:
        t_to = int(request.GET['to'])
    else:
        t_to = None
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
    pass

@RequireLogin
def put(request):
    pass
        

@RequireLogin
def delete(request):
    pass


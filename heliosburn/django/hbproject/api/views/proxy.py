import logging
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from api.models import db_model
from api.models.auth import RequireLogin
from dateutil import parser
from datetime import timedelta
from bson import ObjectId
import re
import time
import json

logger = logging.getLogger(__name__)


@RequireLogin(role='admin')
def status(request):
    """
    Return status of proxy.
    """
    if request.method != "GET":
        return HttpResponse(status=405)

    from api.models import redis_wrapper
    r = redis_wrapper.init_redis()
    response_key = str(ObjectId())
    redis_wrapper.publish_to_proxy(json.dumps({
        "operation": "status",
        "param": None,
        "key": response_key,
    }))
    for i in range(0, 50):
        response = r.get(response_key)
        if response is not None:
            return JsonResponse({"proxyStatus": response})
        else:
            time.sleep(.1)  # sleep 100ms
    return JsonResponse({"proxyStatus": None}, status=503)


@RequireLogin(role='admin')
def start(request):
    """
    Start the proxy.
    """
    if request.method != "GET":
        return HttpResponse(status=405)

    if "session_id" not in request.GET:
        return HttpResponse("session_id required in GET", status=400)
    else:
        try:
            session_id = request.GET['session_id']
        except ValueError:
            return HttpResponse("session_id must be a string", status=400)

    from api.models import redis_wrapper
    r = redis_wrapper.init_redis()
    response_key = str(ObjectId())
    redis_wrapper.publish_to_proxy(json.dumps({
        "operation": "start",
        "param": {"session": session_id},
        "key": response_key,
    }))
    for i in range(0, 50):
        response = r.get(response_key)
        if response is not None:
            return JsonResponse({"proxyResponse": response})
        else:
            time.sleep(.1)  # sleep 100ms
    return JsonResponse({"proxyResponse": None}, status=503)


@RequireLogin(role='admin')
def stop(request):
    """
    Stop the proxy.
    """
    if request.method != "GET":
        return HttpResponse(status=405)

    from api.models import redis_wrapper
    r = redis_wrapper.init_redis()
    response_key = str(ObjectId())
    redis_wrapper.publish_to_proxy(json.dumps({
        "operation": "stop",
        "param": None,
        "key": response_key,
    }))
    for i in range(0, 50):
        response = r.get(response_key)
        if response is not None:
            return JsonResponse({"proxyResponse": response})
        else:
            time.sleep(.1)  # sleep 100ms
    return JsonResponse({"proxyResponse": None}, status=503)
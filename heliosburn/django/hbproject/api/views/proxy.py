import logging
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from api.models import db_model
from api.models.auth import RequireLogin
from dateutil import parser
from datetime import timedelta
from bson import ObjectId
import re
import time

logger = logging.getLogger(__name__)


@RequireLogin(role='admin')
def status_get(request):
    """
    Return status of proxy.
    """
    if request.method != "GET":
        return HttpResponse(status=405)

    from api.models import redis_wrapper
    r = redis_wrapper.init_redis()
    response_key = str(ObjectId())
    redis_wrapper.publish_to_proxy({
        "operation": "status",
        "param": None,
        "key": response_key,
    })
    for i in range(0,50):
        response = r.get(response_key)
        if response is not None:
            return JsonResponse({"proxyStatus": response})
        else:
            time.sleep(.1)  # sleep 100ms
    return JsonResponse({"proxyStatus": None}, status=503)

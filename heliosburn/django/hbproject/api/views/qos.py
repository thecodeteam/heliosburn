import logging
from bson.errors import InvalidId
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, \
    HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
from api.models import db_model, auth
from api.models.auth import RequireLogin
from bson import ObjectId
from datetime import datetime

logger = logging.getLogger(__name__)

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
    except TypeError as inst:
        print inst
        return HttpResponseBadRequest("argument mismatch")


@RequireLogin()
def get(request, qos_id=None):
    """
    Retrieve a QoS profile based on qos_id.
    """
    if qos_id is None:
        return get_all_qos_profiles(request)

    dbc = db_model.connect()
    try:
        qos_profile = dbc.qos.find_one({"_id": ObjectId(qos_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if qos_profile is None:
        return HttpResponseNotFound()

    qos_profile['id'] = str(qos_profile.pop('_id'))
    return JsonResponse(qos_profile)


def get_all_qos_profiles(request):
    """
    Retrieve all QoS profiles.
    """
    dbc = db_model.connect()
    qos_profiles = [q for q in dbc.qos.find()]

    for q in qos_profiles:
        q['id'] = str(q.pop('_id'))
    return JsonResponse({"profiles": qos_profiles})


@RequireLogin()
def post(request):
    """
    Create a new QoS profile.
    """
    try:
        new = json.loads(request.body)
        assert "latency" in new
        assert "name" in new
        assert "jitter" in new
        assert "min" in new["jitter"]
        assert "max" in new["jitter"]
        assert "trafficLoss" in new
    except AssertionError:
        return HttpResponseBadRequest("argument mismatch")
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    dbc = db_model.connect()

    qos_profile = {
        "latency": new['latency'],
        "name": new['name'],
        "jitter": {"min": new['jitter']['min'], "max": new['jitter']['max']},
        "trafficLoss": new['trafficLoss'],
        "createdAt": datetime.isoformat(datetime.now()),
        "updatedAt": datetime.isoformat(datetime.now()),
    }

    if "description" in new:
        qos_profile['description'] = new['description']

    qos_id = str(dbc.qos.save(qos_profile))
    r = JsonResponse({"id": qos_id})
    r['location'] = "/api/qos/%s" % qos_id
    logger.info("qos_profile '%s' created by '%s'" % (qos_id, request.user['username']))
    return r


@RequireLogin()
def put(request, qos_id):
    """
    Update existing qos_profile based on qos_id.
    """
    try:
        new = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    dbc = db_model.connect()
    try:
        qos_profile = dbc.qos.find_one({"_id": ObjectId(qos_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if qos_profile is None:
        return HttpResponseNotFound()

    if "latency" in new:
        qos_profile['latency'] = new['latency']
    if 'name' in new:
        qos_profile['name'] = new['name']
    if 'description' in new:
        qos_profile['description'] = new['description']
    if ("jitter" in new) and ("min" in new['jitter']):
        qos_profile['jitter']['min'] = new['jitter']['min']
    if ("jitter" in new) and ("max" in new['jitter']):
        qos_profile['jitter']['max'] = new['jitter']['max']
    if "trafficLoss" in new:
        qos_profile['trafficLoss'] = new['trafficLoss']


    qos_profile['updatedAt'] = datetime.isoformat(datetime.now())

    dbc.qos.save(qos_profile)
    logger.info("qos_profile '%s' updated by '%s'" % (qos_id, request.user['username']))
    return HttpResponse()


@RequireLogin()
def delete(request, qos_id):
    """
    Delete QoS profile based on qos_id.
    """
    dbc = db_model.connect()
    try:
        qos_profile = dbc.qos.find_one({"_id": ObjectId(qos_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if qos_profile is None:
        return HttpResponseNotFound()

    dbc.qos.remove(qos_profile)
    logger.info("qos_profile '%s' deleted by '%s'" % (qos_id, request.user['username']))
    return HttpResponse()

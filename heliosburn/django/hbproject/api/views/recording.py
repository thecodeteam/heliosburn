import logging
from bson.errors import InvalidId
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import db_model
from bson import ObjectId
from api.models.auth import RequireLogin
import json
from datetime import datetime
import time

logger = logging.getLogger(__name__)


@csrf_exempt
def rest(request, *pargs, **kwargs):
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
        return rest_function(request, *pargs, **kwargs)
    except TypeError:
        return HttpResponseBadRequest("argument mismatch")


@RequireLogin()
def get(request, recording_id=None, get_traffic=None):
    """
    Retrieve recording based on id.
    """
    if recording_id is None:
        return get_all_recordings()
    dbc = db_model.connect()
    try:
        recording = dbc.recording.find_one({"_id": ObjectId(recording_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if recording is None:
        return HttpResponseNotFound()
    else:
        recording['id'] = str(recording.pop('_id'))
        recording['count'] = dbc.traffic.find({"recording_id": recording['id']}).count()

        # Return paginated traffic data
        if get_traffic is not None:

            # Fetch the traffic
            recording['traffic'] = [t for t in dbc.traffic.find({"recording_id": recording['id']})]
            for t in recording['traffic']:
                t['id'] = str(t.pop('_id'))

            # Paginate the traffic
            start = 0
            offset = 100
            if hasattr(request, 'GET') and ('start' in request.GET) and ('offset' in request.GET):
                try:
                    start = int(request.REQUEST['start'])
                    offset = int(request.REQUEST['offset'])
                except ValueError:
                    return HttpResponseBadRequest()

            recording['traffic'] = recording['traffic'][start:(start+offset)]

        return JsonResponse(recording)


def get_all_recordings():
    """
    Retrieve all recordings.
    """
    dbc = db_model.connect()
    recordings = [r for r in dbc.recording.find()]
    for recording in recordings:
        recording['id'] = str(recording.pop('_id'))
        recording['count'] = dbc.traffic.find({"recording_id": recording['id']}).count()
    return JsonResponse({"recordings": recordings})


@RequireLogin()
def post(request):
    """
    Create new recording.
    """

    try:
        in_json = json.loads(request.body)
        assert 'name' in in_json
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    new = {'name': in_json['name']}
    if 'description' in in_json:
        new['description'] = in_json['description']

    dbc = db_model.connect()
    new['createdAt'] = datetime.isoformat(datetime.now())
    new['updatedAt'] = datetime.isoformat(datetime.now())
    recording_id = str(dbc.recording.save(new))
    r = JsonResponse({"id": recording_id})
    r['location'] = "/api/recording/%s" % recording_id
    logger.info("recording '%s' created by '%s'" % (recording_id, request.user['username']))
    return r


@RequireLogin()
def put(request, recording_id):
    """
    Update existing recording based on recording_id.
    """
    try:
        in_json = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    dbc = db_model.connect()
    try:
        recording = dbc.recording.find_one({"_id": ObjectId(recording_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if recording is None:
        return HttpResponseNotFound()
    else:
        if 'name' in in_json:
            recording['name'] = in_json['name']
        if 'description' in in_json:
            recording['description'] = in_json['description']

        recording['updatedAt'] = datetime.isoformat(datetime.now())
        dbc.recording.save(recording)
        r = HttpResponse(status=200)
        r['location'] = "/api/recording/%s" % recording_id
        logger.info("recording '%s' updated by '%s'" % (recording_id, request.user['username']))
        return r


@RequireLogin()
def delete(request, recording_id):
    """
    Delete recording based on recording_id.
    """
    dbc = db_model.connect()
    try:
        recording = dbc.recording.find_one({'_id': ObjectId(recording_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if recording is None:
        return HttpResponseNotFound()
    else:
        dbc.recording.remove({"_id": ObjectId(recording_id)})
        dbc.traffic.remove({"recording_id": recording_id}, multi=True)
        logger.info("recording '%s' deleted by '%s'" % (recording_id, request.user['username']))
        return HttpResponse()


@csrf_exempt
@RequireLogin()
def start(request, recording_id):
    """
    Start a recording, and wait N seconds for the proxy to acknowledge."
    """
    from api.models import redis_wrapper
    r = redis_wrapper.init_redis()
    response_key = str(ObjectId())
    redis_wrapper.publish_to_proxy({
        "operation": "start_recording",
        "param": recording_id,
        "key": response_key,
    })
    logger.info("recording '%s' started by '%s'" % (recording_id, request.user['username']))
    for i in range(0, 50):
        response = r.get(response_key)
        if response is not None:
            return JsonResponse({"proxyResponse": response})
        else:
            time.sleep(.1)  # sleep 100ms
    return JsonResponse({"proxyResponse": None}, status=503)


@csrf_exempt
@RequireLogin()
def stop(request, recording_id):
    """
    Stop a recording, and wait N seconds for the proxy to acknowledge."
    """
    from api.models import redis_wrapper
    r = redis_wrapper.init_redis()
    response_key = str(ObjectId())
    redis_wrapper.publish_to_proxy({
        "operation": "stop_recording",
        "param": recording_id,
        "key": response_key,
    })
    logger.info("recording '%s' stopped by '%s'" % (recording_id, request.user['username']))
    for i in range(0, 50):
        response = r.get(response_key)
        if response is not None:
            return JsonResponse({"proxyResponse": response})
        else:
            time.sleep(.1)  # sleep 100ms
    return JsonResponse({"proxyResponse": None}, status=503)
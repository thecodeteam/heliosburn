from bson.errors import InvalidId
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import db_model
from bson import ObjectId
from api.models.auth import RequireLogin
import json
from datetime import datetime


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
def get(request, recording_id=None):
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
        recording['traffic_count'] = dbc.traffic.find({"recording_id": recording['id']}).count()
        return JsonResponse(recording)


def get_all_recordings():
    """
    Retrieve all recordings.
    """
    dbc = db_model.connect()
    recordings = [r for r in dbc.recording.find()]
    for recording in recordings:
        recording['id'] = str(recording.pop('_id'))
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
        return HttpResponse()


@RequireLogin()
def start(request, recording_id):
    pass  # TODO


@RequireLogin()
def stop(request, recording_id):
    pass  # TODO
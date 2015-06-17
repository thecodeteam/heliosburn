import logging
from bson.errors import InvalidId
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, \
    HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
from api.models import db_model, auth
from api.models.auth import RequireLogin
from bson import ObjectId
from IPython.core.debugger import Tracer
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
def get(request, profile_id=None):
    """
    Retrieve a profile based on profile_id.
    """
    if profile_id is None:
        return get_all_profiles(request)

    dbc = db_model.connect()
    try:
        profile = dbc.serveroverload.find_one({"_id": ObjectId(profile_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if profile is None:
        return HttpResponseNotFound()

    profile['id'] = str(profile.pop('_id'))
    return JsonResponse(profile)


def get_all_profiles(request):
    """
    Retrieve all profiles.
    """
    dbc = db_model.connect()
    profiles = [q for q in dbc.serveroverload.find()]

    for q in profiles:
        q['id'] = str(q.pop('_id'))
    return JsonResponse({"profiles": profiles})


@RequireLogin()
def post(request):
    """
    Create a new profile.
    """
    try:
        new = json.loads(request.body)
        assert "_id" not in new
        assert "name" in new
        assert "description" in new
        assert "function" in new

        p_function = new['function']
        assert "type" in p_function
        assert "expValue" in p_function
        assert "growthRate" in p_function
        assert "response_triggers" in new

        p_response_triggers = new['response_triggers']
        for rt in p_response_triggers:
            assert "fromLoad" in rt
            assert "toLoad" in rt
            assert "actions" in rt
            for action in rt['actions']:
                assert "type" in action
                assert "value" in action
                assert "percentage" in action

    except AssertionError:
        return HttpResponseBadRequest("argument mismatch")
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    new['createdAt'] = datetime.isoformat(datetime.now())
    new['updatedAt'] = datetime.isoformat(datetime.now())
    dbc = db_model.connect()

    profile_id = str(dbc.serveroverload.save(new))
    r = JsonResponse({"id": profile_id})
    r['location'] = "/api/serveroverload/%s" % profile_id
    logger.info("profile '%s' created by '%s'" % (profile_id, request.user['username']))
    return r


@RequireLogin()
def put(request, profile_id):
    """
    Update existing profile based on profile_id.
    """
    try:
        new = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    dbc = db_model.connect()
    profile = dbc.serveroverload.find_one({"_id": ObjectId(profile_id)})
    if profile is None:
        return HttpResponseNotFound()

    # Update provided values
    if "name" in new:
        profile['name'] = new['name']
    if "description" in new:
        profile['description'] = new['description']
    if "function" in new:
        try:
            p_function = new['function']
            if p_function is not None:  # function can be updated as null to "unset" a previous definition
                assert "type" in p_function
                assert "expValue" in p_function
                assert "growthRate" in p_function
                assert "response_triggers" in new
                p_response_triggers = new['response_triggers']
                for rt in p_response_triggers:
                    assert "fromLoad" in rt
                    assert "toLoad" in rt
                    assert "actions" in rt
                    for action in rt['actions']:
                        assert "type" in action
                        assert "value" in action
                        assert "percentage" in action
            profile['function'] = new['function']
        except AssertionError:
            return HttpResponseBadRequest("argument mismatch")

    profile['updatedAt'] = datetime.isoformat(datetime.now())
    dbc.serveroverload.save(profile)
    logger.info("profile '%s' updated by '%s'" % (profile_id, request.user['username']))
    return HttpResponse()


@RequireLogin()
def delete(request, profile_id):
    """
    Delete profile based on profile_id.
    """
    dbc = db_model.connect()
    try:
        profile = dbc.serveroverload.find_one({"_id": ObjectId(profile_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if profile is None:
        return HttpResponseNotFound()

    dbc.serveroverload.remove(profile)
    logger.info("profile '%s' deleted by '%s'" % (profile_id, request.user['username']))
    return HttpResponse()

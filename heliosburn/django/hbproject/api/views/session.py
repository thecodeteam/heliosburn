import logging
from bson.errors import InvalidId
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, \
    HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
from api.models import db_model, auth
from api.models.auth import RequireLogin
from bson import ObjectId
from pymongo.helpers import DuplicateKeyError
from datetime import datetime
import time
from api.models import redis_wrapper

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
def get(request, session_id=None):
    """
    Retrieve a session based on session_id.
    """
    if session_id is None:
        return get_all_sessions(request)

    dbc = db_model.connect()
    try:
        session = dbc.session.find_one({"_id": ObjectId(session_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if session is None:
        return HttpResponseNotFound()

    # Users cannot retrieve sessions they do not own, unless admin
    elif (session['username'] != request.user['username']) and (auth.is_admin(request.user) is False):
        return HttpResponseForbidden()
    else:
        session['id'] = str(session.pop('_id'))
        return JsonResponse(session)


def get_all_sessions(request):
    """
    Retrieve all sessions.
    """
    dbc = db_model.connect()
    if auth.is_admin(request.user) is True:  # Admins retrieve all sessions
        sessions = [s for s in dbc.session.find()]
    else:  # Regular users retrieve only the sessions they own
        sessions = [s for s in dbc.session.find({"username": request.user['username']})]

    for s in sessions:
        s['id'] = str(s.pop('_id'))
    return JsonResponse({"sessions": sessions})


@RequireLogin()
def post(request):
    """
    Create a new session.
    """
    try:
        new = json.loads(request.body)
        assert "name" in new
        assert "description" in new
    except AssertionError:
        return HttpResponseBadRequest("argument mismatch")
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    dbc = db_model.connect()

    session = {
        'name': new['name'],
        'description': new['description'],
        'username': request.user['username'],
        'createdAt': datetime.isoformat(datetime.now()),
        'updatedAt': datetime.isoformat(datetime.now()),
    }

    # Add optional fields
    if "testplan" in new:
        testplan = dbc.testplan.find_one({"_id": ObjectId(new['testplan'])})
        if testplan is not None:
            session['testplan'] = new['testplan']
        else:
            return HttpResponseNotFound("testplan '%s' does not exist" % new['testplan'])

    try:
        session_id = str(dbc.session.save(session))
    except DuplicateKeyError:
        return HttpResponseBadRequest("session name is not unique")
    r = JsonResponse({"id": session_id})
    r['location'] = "/api/session/%s" % session_id
    logger.info("session '%s' created by '%s'" % (session_id, request.user['username']))
    return r


@RequireLogin()
def put(request, session_id):
    """
    Update existing session based on session_id.
    """
    try:
        new = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    dbc = db_model.connect()
    try:
        session = dbc.session.find_one({"_id": ObjectId(session_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if session is None:
        return HttpResponseNotFound()

    # Users can only update their own sessions, unless admin
    elif (session['username'] != request.user['username']) and (auth.is_admin(request.user) is False):
        logger.info("user '%s' attempted to update session '%s', but was forbidden" % (request.user['username'], session_id))
        return HttpResponseForbidden()
    else:
        if "name" in new:
            session['name'] = new['name']
        if "description" in new:
            session['description'] = new['description']
        if "username" in new:
            session['username'] = new['username']
        if "testplan" in new:
            testplan = dbc.testplan.find_one({"_id": ObjectId(new['testplan'])})
            if testplan is not None:
                session['testplan'] = new['testplan']
            else:
                return HttpResponseNotFound("testplan '%s' does not exist" % new['testplan'])
        try:
            session['updatedAt'] = datetime.isoformat(datetime.now())
            dbc.session.save(session)
        except DuplicateKeyError:
            return HttpResponseBadRequest("session name is not unique")
        logger.info("session '%s' updated by '%s'" % (session_id, request.user['username']))
        return HttpResponse()


@RequireLogin()
def delete(request, session_id):
    """
    Delete session based on session_id.
    """
    dbc = db_model.connect()
    try:
        session = dbc.session.find_one({"_id": ObjectId(session_id)})
    except InvalidId:
        return HttpResponseNotFound()
    if session is None:
        return HttpResponseNotFound()

    # Users can only delete their own sessions, unless admin
    elif (session['username'] != request.user['username']) and (auth.is_admin(request.user) is False):
        logger.info("user '%s' attempted to delete session '%s', but was forbidden" % (request.user['username'], session_id))
        return HttpResponseForbidden()
    else:
        dbc.session.remove(session)
        logger.info("session '%s' deleted by '%s'" % (session_id, request.user['username']))
        return HttpResponse()

@csrf_exempt
@RequireLogin()
def start(request, session_id):
    """
    Inform the proxy to start a session based on session_id.
    """
    if request.method != "GET":
        return HttpResponse(status=405)
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
            try:
                response = json.loads(response)
            except ValueError:
                return HttpResponse(status=500)
            if ('code' in response) and (response['code'] == 200):
                return JsonResponse({"proxyResponse": response}, status=200)
            else:
                return HttpResponse(status=500)
        else:
            time.sleep(.1)  # sleep 100ms
    return HttpResponse(status=408)


@csrf_exempt
@RequireLogin()
def stop(request, session_id):
    """
    Inform the proxy to stop a session based on session_id.
    """
    if request.method != "GET":
        return HttpResponse(status=405)
    r = redis_wrapper.init_redis()
    response_key = str(ObjectId())
    redis_wrapper.publish_to_proxy(json.dumps({
        "operation": "stop",
        "param": {"session": session_id},
        "key": response_key,
    }))
    for i in range(0, 50):
        response = r.get(response_key)
        if response is not None:
            try:
                response = json.loads(response)
            except ValueError:
                return HttpResponse(status=500)
            if ('code' in response) and (response['code'] == 200):
                return JsonResponse({"proxyResponse": response}, status=200)
            else:
                return HttpResponse(status=500)
        else:
            time.sleep(.1)  # sleep 100ms
    return HttpResponse(status=408)

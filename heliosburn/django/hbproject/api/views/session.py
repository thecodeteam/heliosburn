from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, \
    HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
from api.models import db_model, auth
from api.models.auth import RequireLogin
from bson import ObjectId
from pymongo.helpers import DuplicateKeyError


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
    session = dbc.session.find_one({"_id": ObjectId(session_id)})
    if session is None:
        return HttpResponseNotFound("", status=404)

    # Users cannot retrieve sessions they do not own, unless admin
    elif (session['username'] != request.user['username']) and (auth.is_admin(request.user) is False):
        return HttpResponseForbidden(status=401)
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
    return JsonResponse({"sessions": sessions}, status=200)


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
        return HttpResponseBadRequest("argument mismatch", status=400)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON", status=400)

    dbc = db_model.connect()

    session = {
        'name': new['name'],
        'description': new['description'],
        'username': request.user['username'],
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
        return HttpResponseBadRequest("session name is not unique", status=409)
    r = JsonResponse({"id": session_id}, status=200)
    r['location'] = "/api/session/%s" % session_id
    return r


@RequireLogin()
def put(request, session_id):
    """
    Update existing session based on session_id.
    """
    try:
        new = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON", status=400)

    dbc = db_model.connect()
    session = dbc.session.find_one({"_id": ObjectId(session_id)})
    if session is None:
        return HttpResponseNotFound(status=404)

    # Users can only update their own sessions, unless admin
    elif (session['username'] != request.user['username']) and (auth.is_admin(request.user) is False):
        return HttpResponseForbidden(status=401)
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
            dbc.session.save(session)
        except DuplicateKeyError:
            return HttpResponseBadRequest("session name is not unique", status=409)
        return HttpResponse(status=200)


@RequireLogin()
def delete(request, session_id):
    """
    Delete session based on session_id.
    """
    dbc = db_model.connect()
    session = dbc.session.find_one({"_id": ObjectId(session_id)})
    if session is None:
        r = JsonResponse({"error": "session_id not found"})
        r.status_code = 404
        return r

    # Users can only delete their own sessions, unless admin
    elif (session['username'] != request.user['username']) and (auth.is_admin(request.user) is False):
        return HttpResponseForbidden(status=401)
    else:
        dbc.session.remove(session)
        return HttpResponse(status=200)

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, \
    HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
from api.models import db_model, auth
from api.models.auth import RequireLogin
from sqlalchemy.exc import IntegrityError
from api.models import db_model


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

    from pymongo.helpers import bson
    dbc = db_model.connect()
    session = dbc.session.find_one({"_id": bson.ObjectId(session_id)}, {"_id": 0})
    if session is None:
        return HttpResponseNotFound("", status=404)

    # Users cannot retrieve sessions they do not own, unless admin
    elif (session['username'] != request.user['username']) and (auth.is_admin(request.user) is False):
        return HttpResponseForbidden(status=401)
    else:
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

    # Replace the _id ObjectId type with a "id" string representing it
    for s in sessions:
        s['id'] = str(s['_id'])
        del s['_id']

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

    session = legacy_db_model.Session(name=new['name'], description=new['description'], user_id=new['user_id'])

    # Add optional column values
    if "testplan_id" in new:
        session.testplan_id = new['testplan_id']

    dbsession.add(session)

    try:
        dbsession.commit()
    except IntegrityError as e:
        return HttpResponseBadRequest("constraint violated", status=409)
    r = JsonResponse({"id": session.id}, status=200)
    r['location'] = "/api/session/%d" % session.id
    return r


@RequireLogin()
def put(request, session_id, dbsession=None):
    """
    Update existing session based on session_id.
    """
    try:
        new = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON", status=400)

    session = dbsession.query(legacy_db_model.Session).filter_by(id=session_id).first()
    if session is None:
        return HttpResponseNotFound(status=404)

    # Users can only update their own sessions, unless admin
    elif (session.user_id != request.user['id']) and (auth.is_admin(request.user['id']) is False):
        return HttpResponseForbidden(status=401)
    else:
        if "name" in new:
            session.name = new['name']
        if "description" in new:
            session.description = new['description']
        if ("user" in new) and ("user_id" in new['user']):
            session.user_id = new['user_id']
        if "testplan_id" in new:
            session.testplan_id = new['testplan_id']
        try:
            dbsession.commit()
        except IntegrityError as e:
            return HttpResponseBadRequest("constraint violated", status=409)
        return HttpResponse(status=200)


@RequireLogin()
def delete(request, session_id, dbsession=None):
    """
    Delete session based on session_id.
    """
    session = dbsession.query(legacy_db_model.Session).filter_by(id=session_id).first()
    if session is None:
        r = JsonResponse({"error": "session_id not found"})
        r.status_code = 404
        return r

    # Users can only delete their own sessions, unless admin
    elif (session.user_id != request.user['id']) and (auth.is_admin(request.user['id']) is False):
        return HttpResponseForbidden(status=401)
    else:
        dbsession.delete(session)
        dbsession.commit()
        return HttpResponse(status=200)


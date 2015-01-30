from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, \
    HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
from api.models import db_model, dbsession, auth
from api.models.auth import RequireLogin
from sqlalchemy.exc import IntegrityError


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

    session = dbsession.query(db_model.Session).filter_by(id=session_id).first()
    if session is None:
        return HttpResponseNotFound("", status=404)

    # Users cannot retrieve sessions they do not own, unless admin
    elif (session.user.id != request.user['id']) and (auth.is_admin(request.user['id']) is False):
        return HttpResponseForbidden(status=401)
    else:
        session_dict = {
            'id': session.id,
            'name': session.name,
            'description': session.description,
            'testPlan': session.testplan,
            'createdAt': session.created_at,
            'updatedAt': session.updated_at,
            'user': {
                "username": session.user.username,
                "email": session.user.email,
            }
        }
        r = JsonResponse(session_dict)
        return r


@RequireLogin()
def get_all_sessions(request):
    """
    Retrieve all sessions.
    """
    if auth.is_admin(request.user['id']) is True:  # Admins retrieve all sessions
        all_sessions = dbsession.query(db_model.Session).all()
    else:  # Regular users retrieve only the sessions they own
        all_sessions = dbsession.query(db_model.Session).filter_by(user_id=request.user['id'])
    session_list = list()
    for session in all_sessions:
        session_dict = {
            'id': session.id,
            'name': session.name,
            'description': session.description,
            'testPlan': session.testplan,
            'createdAt': session.created_at,
            'updatedAt': session.updated_at,
            'user': {
                "username": session.user.username,
                "email": session.user.email,
            },
            "executions": 0  # TODO: get the real value here
        }
        session_list.append(session_dict)

    return JsonResponse({"sessions": session_list}, status=200)


@RequireLogin()
def post(request):
    """
    Create a new session.
    """
    try:
        new = json.loads(request.body)
        assert "name" in new
        if hasattr(request, "user"):
            new['user_id'] = request.user['id']
        else:
            assert "user_id" in new
        assert "description" in new
    except AssertionError:
        return HttpResponseBadRequest("argument mismatch", status=400)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON", status=400)

    session = db_model.Session(name=new['name'], description=new['description'], user_id=new['user_id'])

    # Add optional column values
    if "testplan_id" in new:
        session.testplan_id = new['testplan_id']

    dbsession.add(session)

    try:
        dbsession.commit()
    except IntegrityError as e:
        return HttpResponseBadRequest("constraint violated", status=409)
    return JsonResponse({"id": session.id}, status=200)


@RequireLogin()
def put(request, session_id):
    """
    Update existing session based on session_id.
    """
    try:
        new = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON", status=400)

    session = dbsession.query(db_model.Session).filter_by(id=session_id).first()
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
def delete(request, session_id):
    """
    Delete session based on session_id.
    """
    session = dbsession.query(db_model.Session).filter_by(id=session_id).first()
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


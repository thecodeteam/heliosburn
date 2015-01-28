from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, \
    HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import json
from api.models import db_model
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
        r = HttpResponse('Invalid method.', status=405)
        r['Allow'] = 'GET,POST,PUT,DELETE'
        return r

    try:
        return rest_function(request, *pargs)
    except TypeError as inst:
        return HttpResponseServerError("argument mismatch")


@RequireLogin
def get(request, session_id=None):
    """Retrieve a session."""
    if not session_id:
        return get_all_sessions(request)
    dbsession = db_model.init_db()
    session = dbsession.query(db_model.Session).filter_by(id=session_id).first()
    if not session:
        return HttpResponseNotFound()
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


def get_all_sessions(request):
    """Retrieves all sessions."""
    dbsession = db_model.init_db()
    all_sessions = dbsession.query(db_model.Session).all()
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

    return JsonResponse({"sessions": session_list})


@RequireLogin
def post(request):
    """Create a new session."""
    try:
        new = json.loads(request.body)
        assert "name" in new
        if hasattr(request, "user_id"):
            new['user_id'] = request.user_id
        else:
            assert "user_id" in new
        assert "description" in new
    except AssertionError:
        return HttpResponseBadRequest("argument mismatch")
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    dbsession = db_model.init_db()
    session = db_model.Session(name=new['name'], description=new['description'], user_id=new['user_id'])

    # Add optional column values
    if "testplan_id" in new:
        session.testplan_id = new['testplan_id']

    dbsession.add(session)

    try:
        dbsession.commit()
    except IntegrityError as e:
        return HttpResponseServerError("constraint violated")
    return HttpResponse("", status=201)


@RequireLogin
def put(request, session_id):
    """Update existing session."""
    try:
        new = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    dbsession = db_model.init_db()
    session = dbsession.query(db_model.Session).filter_by(id=session_id).first()
    if not session:
        return HttpResponseNotFound("")
    else:
        if "name" in new:
            session.name = new['name']
        if "description" in new:
            session.description = new['description']
        if "user_id" in new['user']:
            session.user_id = new['user_id']
        if "testplan_id" in new['user']:
            session.testplan_id = new['user_id']
        try:
            dbsession.commit()
        except IntegrityError as e:
            return HttpResponseServerError("constraint violated")
        return HttpResponse()


@RequireLogin
def delete(request, session_id):
    """Delete existing session."""
    dbsession = db_model.init_db()
    session = dbsession.query(db_model.Session).filter_by(id=session_id).first()
    if not session:
        return HttpResponseNotFound("session not found")
    else:
        dbsession.delete(session)
        dbsession.commit()
        return HttpResponse()


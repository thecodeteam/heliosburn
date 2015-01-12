from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
import json
from api import models

from IPython.core.debugger import Tracer

@csrf_exempt
def rest(request, *pargs):
    """
    Calls python function corresponding with HTTP METHOD name. 
    Calls with incomplete arguments will return HTTP 400 with a description and argument list.
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
    except TypeError:
            r = JsonResponse({"error": "argument mismatch"})
            r.status_code = 400 # 400 "BAD REQUEST"
            return r

def get(request, session_id):
    """Retrieve a session."""
    dbsession = models.init_db()
    session = dbsession.query(models.Session).filter_by(id=session_id).first()
    if session is None:
        r = JsonResponse({"error": "session id '%s' not found" % session_id})
        r.status_code = 404
        return r
    else:
        session_dict = {
            'name': session.name,
            'desceription': session.description,
            'created_at': session.created_at,
            'updated_at': session.updated_at,
            'started_at': session.started_at,
            'stopped_at': session.stopped_at,
            }
        r = JsonResponse(session_dict)
        r.status_code = 200
        return r


def post(request):
    """Create a new session."""
    Tracer()()
    try:
        in_json = json.loads(request.body)
        new = {
            'description': '',
            'testplan_id': None,
            }
        new.update(in_json)
    except Exception as e:  # TODO: 
        r = JsonResponse({"error": "required arguments missing"})
        r.status_code = 400
        return r

    dbsession = models.init_db()
    session = dbsession.query(models.Session).filter_by(name=new['name']).first()
    if session is not None:
        r = JsonResponse({"error": "session(name) already exists"})
        r.status_code = 409
        return r
    else:
        session = models.Session(name=new['name'], description=new['description'], testplan_id=new['testplan_id'], user_id=new['user_id'])
        dbsession.add(session)
        dbsession.commit()
        session_dict = {
            'name': session.name,
            'description': session.description,
            'testplan_id': session.testplan_id,
            'user_id': session.user_id,
            }
        r = JsonResponse(session_dict)
        r.status_code = 200
        return r


def put(request):
    """Update existing session."""
    #TODO
    return JsonResponse({"todo": "todo"})
        

def delete(request):
    """Delete existing session."""
    #TODO
    return JsonResponse({"todo": "todo"})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from api import models
import inspect

from IPython.core.debugger import Tracer

@csrf_exempt
def rest(request):
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

    # Call appropriate REST function, passing the conents of request.GET as keyword paremeters
    # Calls that raise a TypeError will return a serialized description and arg list to the client
    try:
        return rest_function(request, **request.GET)
    except TypeError:
            required_arguments = inspect.getargspec(rest_function).args
            required_arguments.remove('request') # Remove the request object, client doesn't need to see this
            description = inspect.getdoc(rest_function)
            r = JsonResponse({"description": description, "arguments": required_arguments})
            r.status_code = 400 # 400 "BAD REQUEST"
            return r

def get(request, name):
    """Retrieve a session."""
    dbsession = models.init_db()
    session = dbsession.query(models.Session).filter_by(name=name[0]).first()
    if session is None:
        r = JsonResponse({"error": "session not found"})
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


def post(request, name, description, testplan_id=None, user_id):
    """Create a new session."""
    dbsession = models.init_db()
    session = dbsession.query(models.Session).filter_by(name=name[0]).first()
    if session is not None:
        r = JsonResponse({"error": "session(name) already exists"})
        r.status_code = 409
        return r
    else:
        if testplan_id is None:
            testplan_id = [None]
        session = models.Session(name=name[0], description=[0], testplan_id=testplan_id[0], user_id=user_id[0])
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

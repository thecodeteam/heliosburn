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
    except TypeError:
            r = JsonResponse({"error": "argument mismatch"})
            r.status_code = 400 # 400 "BAD REQUEST"
            return r

def get(request, session_id=None):
    """Retrieve a session."""
    if session_id is None:
        return get_all_sessions(request)
    conn, cur = models.init_db_pg2()
    cur.execute("""
        SELECT s.*, u.id AS user__id, u.username AS user__username, u.email AS user__email, u.created_at AS user__created_at, u.update_at AS user__update_at 
        FROM public.session AS s
        INNER JOIN public.user AS u ON(s.user_id=u.id)
        WHERE s.id=%s
        LIMIT 1
    """, (session_id,))

    if cur.rowcount < 1:
        r = JsonResponse({"error": "session_id %s not found" % session_id})
        r.status_code = 404
        return r
    else:
        session = cur.fetchone()
        session_dict = {
            'id': session['id'],
            'name': session['name'],
            'description': session['description'],
            'user': {
                        'id': session['user__id'],
                        'username': session['user__username'],
                        'email': session['user__email'],
                        'created_at': session['user__created_at'],
                        'update_at': session['user__update_at'],
                    },
             'created_at': session['created_at'],
             'updated_at': session['updated_at'],
             'started_at': session['started_at'],
             'stopped_at': session['stopped_at'],
             }
        r = JsonResponse(session_dict)
        r.status_code = 200
        return r


def get_all_sessions(request):
    """Retrieves all sessions."""
    conn, cur = models.init_db_pg2()
    cur.execute("""
        SELECT s.*, u.id AS user__id, u.username AS user__username, u.email AS user__email, u.created_at AS user__created_at, u.update_at AS user__update_at 
        FROM public.session AS s
        INNER JOIN public.user AS u ON(s.user_id=u.id)
    """)
    session_list = list()
    for session in cur.fetchall():
        session_list.append({
            'id': session['id'],
            'name': session['name'],
            'description': session['description'],
            'user': {
                        'id': session['user__id'],
                        'username': session['user__username'],
                        'email': session['user__email'],
                        'created_at': session['user__created_at'],
                        'update_at': session['user__update_at'],
                    },
             'created_at': session['created_at'],
             'updated_at': session['updated_at'],
             'started_at': session['started_at'],
             'stopped_at': session['stopped_at'],
            })
    r = JsonResponse({"sessions": session_list})
    r.status_code = 200
    return r


def post(request):
    """Create a new session."""
    try:
        new = json.loads(request.body)
        assert "name" in new
        assert "user_id" in new
        assert "description" in new
        assert "testPlan" in new
        assert "id" in new['testPlan']
    except AssertionError:
        r = JsonResponse({"error": "argument mismatch"})
        r.status_code = 400
        return r
    except ValueError:
        r = JsonResponse({"error": "invalid JSON"})
        r.status_code = 400
        return r

    conn, cur = models.init_db_pg2()
    try:
        from psycopg2 import IntegrityError
        cur.execute("""
            INSERT INTO session(name, description, testplan_id, user_id)
            VALUES(%s,%s,%s,%s)
        """, (new['name'], new['description'], new['testPlan']['id'], new['user_id']))
        r = JsonResponse({})
        r.status_code = 204
        return r
    except IntegrityError as e:
        r = JsonResponse({"error": "session could not be created(%s)" % e})
        r.status_code = 409
        return r
    

def put(request):
    """Update existing session."""
    #TODO
    return JsonResponse({"todo": "todo"})
        

def delete(request):
    """Delete existing session."""
    #TODO
    return JsonResponse({"todo": "todo"})

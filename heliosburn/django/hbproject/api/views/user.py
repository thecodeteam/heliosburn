from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from api import models
import json

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
            r = JsonResponse({"error": "arguments mismatch"})
            r.status_code = 400 # 400 "BAD REQUEST"
            return r

def get(request, username=None):
    """Retrieve a user."""
    if username is None:  # Retrieve all users
        return get_all_users(request)

    conn, cur = models.init_db_pg2()
    cur.execute("""SELECT id, username, email, created_at, update_at FROM public.user WHERE username=%s LIMIT 1""", (username,))
    if cur.rowcount == 0:
        r = JsonResponse({"error": "user not found"})
        r.status_code = 404
        return r
    else:
        r = JsonResponse(dict(cur.fetchone()))
        r.status_code = 200
        return r


def get_all_users(request):
    """Retrieves all users."""
    Tracer()()
    conn, cur = models.init_db_pg2()
    cur.execute("SELECT id, username, email, created_at, update_at FROM public.user")
    user_list = [dict(user) for user in cur.fetchall()]
    r = JsonResponse({"users": user_list})
    r.status_code = 200
    return r


def post(request):
    """Create a new user."""
    try:
        new = json.loads(request.body)
        assert "username" in new
        assert "password" in new
        assert "email" in new
    except AssertionError:
        r = JsonResponse({"error": "argument mismatch"})
        r.status_code = 400
        return r
    except ValueError:
        r = JsonResponse({"error": "invalid JSON"})
        r.status_code = 400
        return r

    conn, cur = models.init_db_pg2()
    cur.execute("SELECT id FROM public.user WHERE username=%s LIMIT 1", (new['username'],))
    if cur.rowcount != 0:
        r = JsonResponse({"error": "user already exists"})
        r.status_code = 409
        return r
    else:
        cur.execute("INSERT INTO public.user (username, email, password) VALUES(%s,%s,%s)",
                    (new['username'], new['email'], new['password'],))
        r = JsonResponse({})
        r.status_code = 204
        return r


def put(request, username):
    """Update existing user with matching username."""
    try:
        in_json = json.loads(request.body)
    except ValueError:
        r = JsonResponse({"error": "invalid JSON"})
        r.status_code = 400
        return r

    conn, cur = models.init_db_pg2()
    cur.execute("SELECT * FROM public.user WHERE username=%s LIMIT 1", (username,))
    if cur.rowcount == 0:
        r = JsonResponse({"error": "user not found"})
        r.status_code = 404
        return r
    else:
        user = dict(cur.fetchone())
        user.update(in_json)
        from psycopg2 import IntegrityError
        try:
            cur.execute("""
                UPDATE public.user SET username=%s, email=%s, password=%s, update_at=NOW()
                WHERE id=%s 
                """, (in_json['username'], in_json['email'], in_json['password'], user['id'],))
        except IntegrityError:
            r = JsonResponse({"error": "new username not available"})
            r.status_code = 409
            return r
        r = JsonResponse({})
        r.status_code = 204
        return r
        

def delete(request, username):
    """Delete existing user matching username."""
    dbsession = models.init_db()
    user = dbsession.query(models.User).filter_by(username=username).first()
    if user is None:
        r = JsonResponse({"error": "user not found"})
        r.status_code = 404
        return r
    else:
        dbsession.delete(user)
        dbsession.commit()
        r = JsonResponse({})
        r.status_code = 204
        return r

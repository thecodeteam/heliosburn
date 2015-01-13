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
            r = JsonResponse({"error": "arguments mismatch"})
            r.status_code = 400 # 400 "BAD REQUEST"
            return r

def get(request, username=None):
    """Retrieve a user."""
    if username is None:  # Retrieve all users
        return get_all_users(request)

    dbsession = models.init_db()
    user = dbsession.query(models.User).filter_by(username=username).first()
    if user is None:
        r = JsonResponse({"error": "user not found"})
        r.status_code = 404
        return r
    else:
        user_dict = {
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at,
            'update_at': user.update_at,
            }
        r = JsonResponse(user_dict)
        r.status_code = 200
        return r


def get_all_users(request):
    """Retrieves all users."""
    Tracer()()
    dbsession = models.init_db()
    all_users = dbsession.query(models.User).all()
    user_list = list()
    for user in all_users:
        user_list.append({
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at,
            'update_at': user.update_at,
            })
    r = JsonResponse({"users": user_list})
    r.status_code = 200
    return r


def post(request):
    """Create a new user."""
    try:
        in_json = json.loads(request.body)
        new = {
            'username': in_json['username'],
            'email': in_json['email'],
            'password': in_json['password'],
            }
    except Exception as e:
        r = JsonResponse({"error": "required arguments missing"})
        r.status_code = 400
        return r

    dbsession = models.init_db()
    user = dbsession.query(models.User).filter_by(username=new['username']).first()
    if user is not None:
        r = JsonResponse({"error": "user already exists"})
        r.status_code = 409
        return r
    else:
        user = models.User(username=new['username'], email=new['email'], password=new['password'])
        dbsession.add(user)
        dbsession.commit()
        user_dict = {
            'username': user.username,
            'email': user.email,
            }
        r = JsonResponse(user_dict)
        r.status_code = 200
        return r


def put(request):
    """Update existing user with matching username."""
    try:
        in_json = json.loads(request.body)
        username = in_json['username']
    except Exception as e:
        r = JsonResponse({"error": "required arguments missing"})
        r.status_code = 400
        return r

    dbsession = models.init_db()
    user = dbsession.query(models.User).filter_by(username=username).first()
    if user is None:
        r = JsonResponse({"error": "user not found"})
        r.status_code = 404
        return r
    else:
        if 'email' in in_json:
            user.email = in_json['email']
        if 'password' in in_json:
            user.password = in_json['password']
        import datetime
        user.update_at = datetime.datetime.now()
        dbsession.commit()
        user_dict = {
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at,
            'update_at': user.update_at,
            }
        r = JsonResponse(user_dict)
        r.status_code = 200
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

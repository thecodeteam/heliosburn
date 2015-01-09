from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from api import models

from IPython.core.debugger import Tracer
@csrf_exempt
def rest(request):
    if request.method == 'GET':
        return get(request, **request.GET)
    elif request.method == 'POST':
        return post(request, **request.GET)
    elif request.method == 'PUT':
        return put(request, **request.GET)
    elif request.method == 'DELETE':
        return delete(request, **request.GET)
    else:
        return JsonResponse({"error": "HTTP METHOD UNKNOWN"})

def get(request, username):
    dbsession = models.init_db()
    user = dbsession.query(models.User).filter_by(username=username[0]).first()
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


def post(request, username, email, password):
    dbsession = models.init_db()
    user = dbsession.query(models.User).filter_by(username=username[0]).first()
    if user is not None:
        r = JsonResponse({"error": "user already exists"})
        r.status_code = 409
        return r
    else:
        user = models.User(username=username[0], email=email[0], password=password[0])
        dbsession.add(user)
        dbsession.commit()
        user_dict = {
            'username': user.username,
            'email': user.email,
            }
        r = JsonResponse(user_dict)
        r.status_code = 200
        return r


def put(request, username, email=None, password=None):
    dbsession = models.init_db()
    user = dbsession.query(models.User).filter_by(username=username[0]).first()
    if user is None:
        r = JsonResponse({"error": "user not found"})
        r.status_code = 404
        return r
    else:
        if email is not None:
            user.email = email[0]
        elif password is not None:
            user.password = password[0]
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
        

def delete(request):
    return JsonResponse({__name__: request.method})

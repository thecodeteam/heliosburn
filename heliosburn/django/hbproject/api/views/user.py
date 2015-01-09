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
    Calls with incomplete arguments will return HTTP 400 with 'required_arguments' containing the spec.
    """
    Tracer()()
    if request.method == 'GET':
        try:
            return get(request, **request.GET)
        except TypeError:
            r = JsonResponse({"required_arguments": inspect.getargspec(get).args})
            r.status_code = 400
            return r
    elif request.method == 'POST':
        try:
            return post(request, **request.GET)
        except TypeError:
            r = JsonResponse({"required_arguments": inspect.getargspec(post).args})
            r.status_code = 400
            return r
    elif request.method == 'PUT':
        try:
            return put(request, **request.GET)
        except TypeError:
            r = JsonResponse({"required_arguments": inspect.getargspec(put).args})
            r.status_code = 400
            return r
    elif request.method == 'DELETE':
        try:
            return put(request, **request.GET)
        except TypeError:
            r = JsonResponse({"required_arguments": inspect.getargspec(put).args})
            r.status_code = 400
            return r
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
    # TODO this call should (possibly) not be accessible to the user, do we want them to be able to delete themselves?
    return JsonResponse({__name__: request.method})

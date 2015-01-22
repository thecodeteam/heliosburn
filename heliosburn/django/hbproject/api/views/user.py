from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy.exc import IntegrityError
from api.models import db_model
from api.models.auth import RequireLogin
import hashlib
import json


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
    except TypeError as e:
            print e
            return HttpResponseBadRequest("unknown method")


@RequireLogin
def get(request, username=None):
    """Retrieve a user."""
    if username is None:  # Retrieve all users
        return get_all_users(request)

    dbsession = db_model.init_db()
    user = dbsession.query(db_model.User).filter_by(username=username).first()
    if user is None:
        return HttpResponseNotFound("", status=404)
    else:
        user_dict = {
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at,
            'update_at': user.update_at,
            }
        return JsonResponse(user_dict, status=200)


def get_all_users(request):
    """Retrieves all users."""
    dbsession = db_model.init_db()
    all_users = dbsession.query(db_model.User).all()
    user_list = list()
    for user in all_users:
        user_list.append({
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at,
            'update_at': user.update_at,
            })
    return JsonResponse({"users": user_list}, status=200)


@RequireLogin
def post(request):
    """Create a new user."""
    try:
        new = json.loads(request.body)
        assert "username" in new
        assert "password" in new
        assert "email" in new
    except AssertionError:
        return HttpResponseBadRequest("argument mismatch", status=400)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON", status=400)

    dbsession = db_model.init_db()
    user = dbsession.query(db_model.User).filter_by(username=new['username']).first()
    if user is not None:
        return HttpResponseBadRequest("user already exists")
    else:
        m = hashlib.sha512()
        m.update(new['password'])
        user = db_model.User(username=new['username'], email=new['email'], password=m.hexdigest())
        dbsession.add(user)
        dbsession.commit()
        return HttpResponse("", status=204)


@RequireLogin
def put(request, username):
    """Update existing user with matching username."""
    try:
        in_json = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON", status=400)

    dbsession = db_model.init_db()
    user = dbsession.query(db_model.User).filter_by(username=username).first()
    if user is None:
        return HttpResponseNotFound("")
    else:
        if "username" in in_json:
            user.username = in_json['username']
        if "password" in in_json:
            m = hashlib.sha512()
            m.update(in_json['password'])
            user.password = m.hexdigest()
        if "email" in in_json:
            user.email = in_json['email']
        try:
            dbsession.commit()
        except IntegrityError:
            return HttpResponseBadRequest("user already exists", status=409)
        return HttpResponse("", status=204)
        

@RequireLogin
def delete(request, username):
    """Delete existing user matching username."""
    dbsession = db_model.init_db()
    user = dbsession.query(db_model.User).filter_by(username=username).first()
    if user is None:
        return HttpResponseNotFound("user not found", status=404)
    else:
        dbsession.delete(user)
        dbsession.commit()
        return HttpResponse("", status=204)


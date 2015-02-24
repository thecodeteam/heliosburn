from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from api.models import auth
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


@RequireLogin()
def get(request, username=None):
    """
    Retrieve user based on username.
    """
    if username is None:  # Retrieve all users
        return get_all_users()

    # Users can only retrieve their own account, unless admin
    if (request.user['username'] != username) and (auth.is_admin(request.user) is False):
        return HttpResponseForbidden(status=401)

    from api.models import db_model
    dbc = db_model.connect()
    user = dbc.user.find_one({"username": username}, {"_id": 0})
    if user is None:
        return HttpResponseNotFound(status=404)
    else:
        return JsonResponse(user, status=200)


@RequireLogin(role='admin')
def get_all_users(request):
    """
    Retrieve all users.
    """
    from api.models import db_model
    dbc = db_model.connect()
    return JsonResponse({"users": [user for user in dbc.user.find({}, {"_id": 0})]}, status=200)


@RequireLogin(role='admin')
def post(request):
    """
    Create a new user.
    """
    try:
        new = json.loads(request.body)
        assert "username" in new
        assert "password" in new
        assert "email" in new
    except AssertionError:
        return HttpResponseBadRequest("argument mismatch", status=400)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON", status=400)

    from api.models import db_model
    dbc = db_model.connect()
    user = dbc.user.find_one({"username": new['username']})
    if user is not None:
        return HttpResponseBadRequest("user already exists")
    else:
        m = hashlib.sha512()
        m.update(new['password'])
        dbc.user.save({
            'username': new['username'],
            'email': new['email'],
            'password': m.hexdigest()
        })
        r = HttpResponse(status=200)
        r['location'] = "/api/user/%s" % new['username']
        return r


@RequireLogin()
def put(request, username):
    """
    Update existing user based on username.
    """
    # Users can only update their own account, unless admin
    if (request.user['username'] != username) and (auth.is_admin(request.user) is False):
        return HttpResponseForbidden(status=401)

    try:
        in_json = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON", status=400)

    from api.models import db_model
    dbc = db_model.connect()
    user = dbc.user.find_one({"username": username})
    if user is None:
        return HttpResponseNotFound("")
    else:
        if "password" in in_json:
            m = hashlib.sha512()
            m.update(in_json['password'])
            user['password'] = m.hexdigest()
        if "email" in in_json:
            user['email'] = in_json['email']
        dbc.user.save(user)
        return HttpResponse(status=200)
        

@RequireLogin(role='admin')
def delete(request, username):
    """
    Delete user based on username.
    """
    from api.models import db_model
    dbc = db_model.connect()
    user = dbc.user.find_one({"username": username})
    if user is None:
        return HttpResponseNotFound("user not found", status=404)
    else:
        dbc.user.remove(user)
        return HttpResponse(status=200)

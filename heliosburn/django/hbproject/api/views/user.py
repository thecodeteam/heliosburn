import logging
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from api.models import auth
from api.models.auth import RequireLogin
import hashlib
import json
from datetime import datetime

logger = logging.getLogger(__name__)


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
        return get_all_users(request)

    # Users can only retrieve their own account, unless admin
    if (request.user['username'] != username) and (auth.is_admin(request.user) is False):
        return HttpResponseForbidden()

    from api.models import db_model
    dbc = db_model.connect()
    user = dbc.hbuser.find_one({"username": username}, {"_id": 0})
    if user is None:
        return HttpResponseNotFound()
    else:
        return JsonResponse(user)


@RequireLogin(role='admin')
def get_all_users(request):
    """
    Retrieve all users.
    """
    from api.models import db_model
    dbc = db_model.connect()
    return JsonResponse({"users": [user for user in dbc.hbuser.find({}, {"_id": 0})]})


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
        return HttpResponseBadRequest("argument mismatch")
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    from api.models import db_model
    dbc = db_model.connect()
    user = dbc.hbuser.find_one({"username": new['username']})
    if user is not None:
        return HttpResponseBadRequest("user already exists")
    else:
        m = hashlib.sha512()
        m.update(new['password'])
        dbc.hbuser.save({
            'username': new['username'],
            'email': new['email'],
            'password': m.hexdigest(),
            'createdAt': datetime.isoformat(datetime.now()),
            'updatedAt': datetime.isoformat(datetime.now()),
        })
        r = HttpResponse(status=200)
        r['location'] = "/api/user/%s" % new['username']
        logger.info("user '%s' created by '%s'" % (new['username'], request.user['username']))
        return r


@RequireLogin()
def put(request, username):
    """
    Update existing user based on username.
    """
    # Users can only update their own account, unless admin
    if (request.user['username'] != username) and (auth.is_admin(request.user) is False):
        return HttpResponseForbidden()

    try:
        in_json = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest("invalid JSON")

    from api.models import db_model
    dbc = db_model.connect()
    user = dbc.hbuser.find_one({"username": username})
    if user is None:
        return HttpResponseNotFound()
    else:
        if "password" in in_json:
            m = hashlib.sha512()
            m.update(in_json['password'])
            user['password'] = m.hexdigest()
        if "email" in in_json:
            user['email'] = in_json['email']
        user['updatedAt'] = datetime.isoformat(datetime.now())
        dbc.hbuser.save(user)
        logger.info("user '%s' updated by '%s'" % (username, request.user['username']))
        return HttpResponse()
        

@RequireLogin(role='admin')
def delete(request, username):
    """
    Delete user based on username.
    """
    from api.models import db_model
    dbc = db_model.connect()
    user = dbc.hbuser.find_one({"username": username})
    if user is None:
        return HttpResponseNotFound("user not found")
    else:
        dbc.hbuser.remove(user)
        logger.info("user '%s' deleted by '%s'" % (username, request.user['username']))
        return HttpResponse()

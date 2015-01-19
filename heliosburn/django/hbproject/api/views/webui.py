from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api import models
import json
import hashlib

@csrf_exempt
def authenticate(request):
    """
    Authenticates given 'username' and 'password_hash' against user in database.
    """
    try:
        in_json = json.loads(request.body)
        assert "username" in in_json
        assert "password_hash" in in_json
    except AssertionError:
        r = JsonResponse({"error": "argument mismatch"})
        r.status_code = 400
        return r
    except ValueError as e:
        r = JsonResponse({"error": "invalid JSON"})
        r.status_code = 400
        return r

    dbsession = models.init_db()
    user = dbsession.query(models.User).filter_by(username=in_json['username']).first()
    if user is None:
        r = JsonResponse({"error": "user not found"})
        r.status_code = 404
        return r
    else:
        m = hashlib.sha512()
        m.update(user.password.encode())
        password_hash = m.hexdigest().encode()
        if in_json['password_hash'] == password_hash:
            r = JsonResponse({})
            r.status_code = 204
            return r
        else:
            r = JsonResponse({})
            r.status_code = 403
            return r

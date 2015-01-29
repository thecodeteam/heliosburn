import json
import hashlib
import os
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from api.models import db_model, dbsession


@csrf_exempt
def login(request):
    """
    Authenticates given 'username' and 'password_hash' against user in database.
    """
    if request.method != 'POST':
        r = HttpResponse('Invalid method. Only POST method accepted.', status=405)
        r['Allow'] = 'POST'
        return r
    
    try:
        in_json = json.loads(request.body)
        assert "username" in in_json
        assert "password" in in_json
    except AssertionError:
        return HttpResponseBadRequest("argument mismatch")
    except ValueError as e:
        return HttpResponseBadRequest("invalid JSON")

    user = dbsession.query(db_model.User).filter_by(username=in_json['username']).first()
    if not user:
        # not returning "user not found" to avoid attackers to guess valid users
        return HttpResponse(status=401)
    else:
        m = hashlib.sha512()
        m.update(in_json['password'])
        password_hash = m.hexdigest()
        if user.password == password_hash:
            m = hashlib.sha512()
            m.update(os.urandom(64))
            token_string = m.hexdigest()
            from api.models import redis_wrapper
            r = redis_wrapper.init_redis()
            r.set(token_string, user.id, settings.TOKEN_TTL)  # Store tokens to expire in 1 hour
            r = HttpResponse()
            r['X-Auth-Token'] = token_string
            return r
        else:
            return HttpResponse(status=401)

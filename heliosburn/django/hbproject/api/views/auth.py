from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import db_model
import json
import hashlib
import os
from datetime import datetime

@csrf_exempt
def login(request):
    """
    Authenticates given 'username' and 'password_hash' against user in database.
    """
    try:
        in_json = json.loads(request.body)
        assert "username" in in_json
        assert "password" in in_json
    except AssertionError:
        r = JsonResponse({"error": "argument mismatch"})
        r.status_code = 400
        return r
    except ValueError as e:
        r = JsonResponse({"error": "invalid JSON"})
        r.status_code = 400
        return r

    dbsession = db_model.init_db()
    user = dbsession.query(db_model.User).filter_by(username=in_json['username']).first()
    if user is None:
        r = JsonResponse({"error": "user not found"})
        r.status_code = 404
        return r
    else:
        m = hashlib.sha512()
        m.update(in_json['password'])
        password_hash = m.hexdigest()
        if user.password == password_hash:
            m = hashlib.sha512()
            m.update(os.urandom(64))
            token_string = m.hexdigest()
            user.token = token_string
            user.token_created_at = datetime.now()
            dbsession.commit()
            r = JsonResponse({})
            r['X-Auth-Token'] = token_string
            r.status_code = 204
            return r
        else:
            r = JsonResponse({})
            r.status_code = 403
            return r

# Model to contain authentication and authorization related assets


def is_admin(user_id):
    """
    Tests for 'admin' on a user_id. Returns True/False.
    """
    # Notes to other devs: Do not be tempted to re-write this as a decorator! While a decorator would make
    # adding @RequireAdmin very convenient, we could no longer use it to decide which action to take when
    # the result of an API call would be different for an admin VS a regular user.
    # When written as a True/False returning function, we can use more flexible code such as:
    #   if is_admin() is True:
    #       do_something_drastic()
    #   else:
    #       do_something_less_drastic()
    from api.models import dbsession, db_model
    user = dbsession.query(db_model.User).filter_by(id=user_id, admin=True).first()
    if user is None:
        return False
    else:
        return True


class RequireLogin(object):
    """
    This decorator inspects incoming HTTP request dictionaries for a X-AUTH-TOKEN header.

    If the token is found, it is validated. If the token is invalid or missing, http 401 is returned.
    """
    def __init__(self, f):
        self.f = f
        self.token_string = "INVALID"  # valid string that will always fail to validate
        self.user_id = None

    def __call__(self, request, *pargs, **kwargs):
        if 'HTTP_X_AUTH_TOKEN' in request.META:
            if type(request.META['HTTP_X_AUTH_TOKEN']) is tuple:  # Unit test's "request" module uses a tuple for headers
                self.token_string = request.META['HTTP_X_AUTH_TOKEN'][1]
            else:  # Real requests do not use a tuple for headers
                self.token_string = request.META['HTTP_X_AUTH_TOKEN']
            if self.valid_token():
                request.user_id = self.user_id
                request.token_string = self.token_string
                return self.f(request, *pargs, **kwargs)

        # 401 Unauthorized if you reach this point
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden(status=401)

    def valid_token(self):
        """
        Validate token in self.token_string against redis backend.
        """
        from api.models import redis_wrapper
        from django.conf import settings

        r = redis_wrapper.init_redis()
        user_id = r.get(self.token_string)
        if not user_id:
            return False
        else:
            self.user_id = int(user_id)
            r.expire(self.token_string, settings.TOKEN_TTL)  # renew the token expiration
            return True
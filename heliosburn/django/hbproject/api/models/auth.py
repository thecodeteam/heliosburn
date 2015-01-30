# Model to contain authentication and authorization related assets


def is_admin(user_id):
    """
    Tests for 'admin' role on a user_id. Returns True/False.
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
    user = dbsession.query(db_model.User).filter_by(id=user_id).first()
    if user.user_role.name is None:  # no role set?
        return False
    elif user.user_role.name == "admin":  # role set to admin
        return True
    else:  # role set, but not admin
        return False


class RequireLogin(object):
    """
    This decorator inspects incoming HTTP request dictionaries for a X-AUTH-TOKEN header.

    If the token is found, it is validated. If the token is invalid or missing, http 401 is returned.
    """

    def __init__(self, f):
        self.f = f
        self.token_string = "INVALID"  # valid string that will always fail to validate
        self.user_id = None
        self.username = None
        self.user_role = None

    def __call__(self, request, *pargs, **kwargs):
        from django.http import HttpResponseForbidden

        if 'HTTP_X_AUTH_TOKEN' in request.META:
            self.token_string = request.META['HTTP_X_AUTH_TOKEN']
            if self.valid_token():
                user = self.fetch_user()
                if user is None:  # The user matching the token has been deleted
                    return HttpResponseForbidden(status=401)
                request.user = {
                    'id': self.user_id,
                    'username': self.username,
                    'user_role': self.user_role,
                    }
                request.token_string = self.token_string
                return self.f(request, *pargs, **kwargs)

        # 401 Unauthorized if you reach this point

        return HttpResponseForbidden(status=401)

    def fetch_user(self):
        """
        Populate self.user_id, self.username, self.user_role with user information.
        """
        from api.models import dbsession, db_model
        user = dbsession.query(db_model.User).filter_by(id=self.user_id).first()
        if user is None:  # User not in database means they were deleted, but (still) have a valid token
            return False
        self.username = user.username
        self.user_role = user.user_role.name
        return True



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
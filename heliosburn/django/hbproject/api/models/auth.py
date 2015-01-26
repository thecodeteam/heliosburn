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
            self.token_string = request.environ['HTTP_X_AUTH_TOKEN']
            if self.valid_token():
                request.user_id = self.user_id
                request.token_string = self.token_string
                return self.f(request)

        # 401 Unauthorized if you reach this point
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("", status=401)


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
class RequireLogin(object):
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
        from django.http import HttpResponse

        return HttpResponse(status=401)

    def valid_token(self):
        from api.models import redis_wrapper

        r = redis_wrapper.init_redis()
        user_id = r.get(self.token_string)
        print self.token_string
        if not user_id:
            return False
        else:
            self.user_id = int(user_id)
            r.expire(self.token_string, 3600)  # renew the token expiration
            return True
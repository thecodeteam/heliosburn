class RequireLogin(object):

    def __init__(self, f):
        self.f = f
        self.token_string = "INVALID"  # valid string that will always fail to validate

    def __call__(self, request, *pargs, **kwargs):
        if 'HTTP_X_AUTH_TOKEN' in request.META:
            self.token_string = request.environ['HTTP_X_AUTH_TOKEN']
            if self.valid_token_redis():
                return self.f(request)

        # 403 forbidden if you reach this point
        from django.http import JsonResponse
        r = JsonResponse({})
        r.status_code = 403
        return r

    def valid_token(self):  # TODO: DEPRECATED, remove this once redis is 100% confirmed for tokens
        import db_model
        dbsession = db_model.init_db()
        user = dbsession.query(db_model.User).filter_by(token=self.token_string).first()
        if user is None:
            return False
        else:
            return True

    def valid_token_redis(self):
        from api.models import redis_wrapper
        r = redis_wrapper.init_redis(1)
        r = r.get(self.token_string)
        if r is None:
            return False
        else:
            return True
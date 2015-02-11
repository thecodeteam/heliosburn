from django.http import HttpResponseServerError
from models import dbsession


class RequireDB(object):
    """
    This decorator initializes a DB session and closes it after the function exits.
    """

    def __call__(self, f):
        self.f = f

        def wrapped_f(request, *pargs, **kwargs):
            session = dbsession()
            kwargs['dbsession'] = dbsession
            try:
                return self.f(request, *pargs, **kwargs)
            except:
                session.rollback()
                return HttpResponseServerError()
            finally:
                session.close()
        return wrapped_f

from django.http import HttpResponseServerError
from models import dbsession
from sqlalchemy.exc import SQLAlchemyError


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
            except SQLAlchemyError as e:
                session.rollback()
                return HttpResponseServerError("database error: %s" % e)
            finally:
                session.close()
        return wrapped_f

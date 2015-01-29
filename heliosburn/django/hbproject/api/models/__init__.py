from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker

dbsession = scoped_session(sessionmaker())
engine = create_engine("postgresql://%s:%s@%s/%s" % (
    settings.DATABASES['default']['USER'],
    settings.DATABASES['default']['PASSWORD'],
    settings.DATABASES['default']['HOST'],
    settings.DATABASES['default']['NAME'],
    ))
dbsession.configure(bind=engine, autoflush=False, expire_on_commit=False)
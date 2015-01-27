from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
import db_model
import hashlib

dbsession = scoped_session(sessionmaker())
engine = create_engine("postgresql://postgres:postgres@localhost/heliosburn")
dbsession.configure(bind=engine, autoflush=False, expire_on_commit=False)

db_model.Base.metadata.drop_all(engine)
db_model.Base.metadata.create_all(engine)
m = hashlib.sha512()
m.update("admin")
admin_user = db_model.User(username='admin', password=m.hexdigest(), email="admin@local")
dbsession.add(admin_user)
dbsession.commit()
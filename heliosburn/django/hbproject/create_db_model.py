
def main():
    from django.conf import settings
    from hbproject import settings as hb_settings
    settings.configure(default_settings=hb_settings)
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
######################## pasted in above, delete this later
    import hashlib
    from api.models import db_model

    db_model.Base.metadata.drop_all(engine)
    db_model.Base.metadata.create_all(engine)

    print("Creating 'admin' role")
    admin_role = db_model.UserRole(name='admin')

    print("Creating an initial user named 'admin' with password 'admin' with role 'admin'")
    m = hashlib.sha512()
    m.update("admin")
    admin_user = db_model.User(username='admin', password=m.hexdigest(), email="admin@local", user_role=admin_role)
    dbsession.add(admin_user)

    print("Creating an initial user named 'test1' with password 'test1' with no role")
    m = hashlib.sha512()
    m.update("test1")
    test_user = db_model.User(username='test1', password=m.hexdigest(), email="test1@local")
    dbsession.add(test_user)
    dbsession.commit()

if __name__ == '__main__':
    main()
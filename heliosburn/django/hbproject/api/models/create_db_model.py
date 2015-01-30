
def main():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session
    from sqlalchemy.orm.session import sessionmaker
    import hashlib
    from api.models import db_model, dbsession, engine

    db_model.Base.metadata.drop_all(engine)
    db_model.Base.metadata.create_all(engine)

    m = hashlib.sha512()
    m.update("admin")

    print("Creating 'admin' role")
    admin_role = db_model.UserRole(name='admin')

    print("Creating an initial user named 'admin' with password 'admin' with role 'admin'")
    admin_user = db_model.User(username='admin', password=m.hexdigest(), email="admin@local", user_role=admin_role)
    dbsession.add(admin_user)
    dbsession.commit()

if __name__ == '__main__':
    main()
def main():
    from hbproject import settings as s

    import pymongo

    dbc = pymongo.Connection()
    for db in s.MONGODB_DATABASE.keys():
        print("Dropping database '%s': %s" % (db, s.MONGODB_DATABASE[db]))
        dbc.drop_database(s.MONGODB_DATABASE[db])


    # Initial roles
    roles = [
        {"name": "admin"},
    ]

    # Initial users
    import hashlib
    hasher1 = hashlib.sha512()
    hasher1.update("admin")
    hasher2 = hashlib.sha512()
    admin_hash = hasher1.hexdigest()
    hasher2.update("test1")
    test1_hash = hasher2.hexdigest()
    users = [
        {
            "username": "admin",
            "password": admin_hash,
            "email": "admin@local",
            "roles": ["admin"],
        },
        {
            "username": "test1",
            "password": test1_hash,
            "email": "test1@local",
            "roles": ["standard"],
        },
    ]

    # Initial roles
    roles = [
        {"name": "admin"},
        {"name": "standard"},
    ]

    for db in s.MONGODB_DATABASE.keys():
        current_db = dbc[s.MONGODB_DATABASE[db]]

        print("Creating users in db '%s': %s" % (db, s.MONGODB_DATABASE[db]))
        for user in users:
            current_db.hbuser.save(user)

        print("Creating roles in db '%s': %s" % (db, s.MONGODB_DATABASE[db]))
        for role in roles:
            current_db.role.save(role)

        print("Creating indexes in db '%s': %s" % (db, s.MONGODB_DATABASE[db]))
        current_db.hbuser.ensure_index('username', unique=True)
        current_db.testplan.ensure_index('name', unique=True)
        current_db.session.ensure_index('name', unique=True)

if __name__ == '__main__':
    main()
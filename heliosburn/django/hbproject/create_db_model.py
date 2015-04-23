import os
import dotenv
from configurations import importer
import pymongo
from datetime import datetime

dotenv.read_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hbproject.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')

importer.install()

from hbproject import settings as s


def main():
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
    admin_hash = hasher1.hexdigest()

    hasher2 = hashlib.sha512()
    hasher2.update("test1")
    test1_hash = hasher2.hexdigest()
    users = [
        {
            "username": "admin",
            "password": admin_hash,
            "email": "admin@local",
            "roles": ["admin"],
            "createdAt": datetime.isoformat(datetime.now()),
            "updatedAt": datetime.isoformat(datetime.now()),
        },
        {
            "username": "test1",
            "password": test1_hash,
            "email": "test1@local",
            "roles": ["standard"],
            "createdAt": datetime.isoformat(datetime.now()),
            "updatedAt": datetime.isoformat(datetime.now()),
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
        current_db.template.ensure_index('name', unique=True)
        current_db.traffic.ensure_index('recording_id')

        print("Creating capped collection 'log' in db '%s'" % s.MONGODB_DATABASE[db])
        current_db.create_collection('log', capped=True, size=500000)
        print("Indexing log.timestamp in db '%s'" % s.MONGODB_DATABASE[db])
        current_db.log.ensure_index('timestamp')

if __name__ == '__main__':
    main()

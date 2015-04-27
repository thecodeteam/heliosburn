def connect(database_name='production'):
    """
    Returns MongoClient connected to database provided as keyword argument 'database_name'.
    """
    from pymongo import MongoClient
    from hbproject import settings as s


    # Reliably test if django unit tests are being ran and use test database if so
    import sys
    if 'test' in sys.argv:
        database_name = 'test'

    client = MongoClient(host=s.MONGODB_HOST, port=s.MONGODB_PORT)
    return client[s.MONGODB_DATABASE[database_name]]

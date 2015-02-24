def connect(database_name='production'):
    """
    Returns MongoClient connected to database provided as keyword argument 'database_name'.
    """
    from pymongo import MongoClient
    from hbproject import settings as s
    client = MongoClient(host=s.MONGODB_HOST, port=s.MONGODB_PORT)
    return client[s.MONGODB_DATABASE[database_name]]

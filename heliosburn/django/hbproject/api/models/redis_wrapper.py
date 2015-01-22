def init_redis(db=0):
    """
    Returns redis connection. Default db is 0 unless db=<n> is passed.
    """
    import redis
    return redis.StrictRedis('localhost', db=db)
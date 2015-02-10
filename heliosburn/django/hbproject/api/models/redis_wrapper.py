from django.conf import settings


def init_redis():
    """
    Returns redis connection.
    """
    import redis
    return redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def publish_to_proxy(msg):
    r = init_redis()
    r.publish('proxy_core', msg)
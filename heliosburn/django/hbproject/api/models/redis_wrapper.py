from django.conf import settings


def init_log():
    from redislog import handlers, logger
    l = logger.RedisLogger('hb.logger')
    l.setLevel(logger.logging.DEBUG)
    l.addHandler(handlers.RedisHandler.to('hblog'))
    return l


def init_redis():
    """
    Returns redis connection.
    """
    import redis
    return redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def publish_to_proxy(msg):
    r = init_redis()
    r.publish('proxy_mgmt_request', msg)

logger = init_log()  # This line allows `from api.models.redis_wrapper import logger` - for convenience
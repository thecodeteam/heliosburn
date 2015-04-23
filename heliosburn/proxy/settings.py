

from configurations import Configuration, values
import redis


class Common(Configuration):
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'redis': {
                'level': 'DEBUG',
                'class': 'redislog.handlers.RedisHandler',
                'channel': 'hblog',
                'redis_client': redis.Redis(host=REDIS_HOST,
                                            port=REDIS_PORT,
                                            db=REDIS_DB),
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'INFO',
            },
            'webui': {
                'handlers': ['console', 'redis'],
                'level': 'DEBUG',
            },
            'api': {
                'handlers': ['console', 'redis'],
                'level': 'DEBUG',
            },
            'proxy': {
                'handlers': ['console', 'redis'],
                'level': 'DEBUG',
            },
        }
    }


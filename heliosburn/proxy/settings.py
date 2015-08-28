

from configurations import Configuration
import redis


class Common(Configuration):
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_KEY = 'hb.traffic'
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_DB = 'heliosburn'

    PROXY = {
        'proxy_address': '127.0.0.1',
        'proxy_port': 8880,
        'upstream_host': '209.118.208.30',
        'upstream_port': 80,
        'redis_host': REDIS_HOST,
        'redis_port': REDIS_PORT,
        'redis_db': REDIS_DB,
        'redis_key': REDIS_KEY,
        'mongo_host': MONGO_HOST,
        'mongo_port':  MONGO_PORT,
        'mongo_db':  MONGO_DB,
        'traffic_pub_queue': 'heliosburn.traffic',
        'traffic_sub_queue': 'heliosburn.traffic',
        'control_pub_queue': 'proxy_mgmt_request',
        'control_sub_queue': 'proxy_mgmt_response',
        'echo_server_port': 7599,
        'plugins': {
            'support': [
                'TrafficReader',
                'TrafficStream',
                'TrafficRecorder'
            ],
            'session': [
                'QOS',
                'ServerOverload',
                'Injection'
            ],
            'test': [
                'TestStopRecordingAPI',
                # 'TestStartSessionAPI',
                # 'TestStopSessionAPI',
                'TestStopProxyAPI',
                'TestStartProxyAPI',
                'TestChangeUpstreamHostAPI',
                'TestChangeUpstreamPortAPI',
                'TestChangeBindAddressAPI',
                'TestChangeBindPortAPI',
                'TestResetPluginsAPI',
                'TestReloadPluginsAPI',
                'TestStatusAPI',
                'TestBusyRecordingAPI',
            ],
        }
    }

    FORMAT = "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': FORMAT,
                'datefmt': "%d/%b/%Y %H:%M:%S"
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

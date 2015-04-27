from module import AbstractModule
import time
import json
import redis
from protocols.redis import HBRedisSubscriberFactory
from protocols.redis import HBRedisMessageHandlerFactory
from protocols.redis import HBRedisMessageHandler
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor
from twisted.python import log


class TrafficHandler(HBRedisMessageHandler):

    def _get_current_time(self):
        return int(time.time() * 1000000)

    def execute(self):
        r = redis.StrictRedis(host=self.configs['redis_host'],
                              port=self.configs['redis_port'],
                              db=self.configs['redis_db'])
        redis_key = self.configs['redis_key']

        score = self._get_current_time()

        # Remove traffic older than 1 second
        result = r.zremrangebyscore(redis_key, '-inf',
                                    score - 1 * 1000000)
        self.log.msg('* Cleaned %d messages' % (result,))

        result = r.zadd(redis_key, score, self.message)
        if result:
            self.log.msg('* Message with score %d sent successfully'
                         % (score,))
        else:
            self.log.msg('Could not send message (%d)' % (score,))


class TrafficStream(AbstractModule):
    """
    Extension of AbstractModule class used to serialize items to Redis.
    """
    def __init__(self):
        AbstractModule.__init__(self)

    def _subscribe(self, redis):
        self.redis_subscriber = redis
        redis.subscribe()

    def configure(self, **configs):
        self.configs = configs
        self.channel = configs['redis_sub_queue']
        self.start()

    def start(self, **params):
        self.redis_endpoint = TCP4ClientEndpoint(reactor,
                                                 self.configs['redis_host'],
                                                 self.configs['redis_port'])
        handler_factory = HBRedisMessageHandlerFactory(TrafficHandler,
                                                       **self.configs)
        d = self.redis_endpoint.connect(HBRedisSubscriberFactory(self.channel,
                                        handler_factory))

        d.addCallback(self._subscribe)

    def stop(self, **params):
        if self.redis_subscriber:
            self.redis_subscriber.unsubscribe()


traffic_stream = TrafficStream()

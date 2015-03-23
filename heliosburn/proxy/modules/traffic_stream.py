from module import AbstractModule
import time
import json
import redis
from redis_subscriber import HBRedisSubscriberFactory
from redis_subscriber import HBRedisMessageHandlerFactory
from redis_subscriber import HBRedisMessageHandler
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor


class TrafficHandler(HBRedisMessageHandler):

    def _get_current_time(self):
        return int(time.time() * 1000000)

    def execute(self):
        r = redis.StrictRedis(host='127.0.0.1',
                              port=6379,
                              db=0)

        score = self._get_current_time()

        # Remove traffic older than 1 second
        result = r.zremrangebyscore('heliosburn.traffic', '-inf',
                                    score - 1 * 1000000)
        self.log.msg('* Cleaned %d messages' % (result,))

        result = r.zadd('heliosburn.traffic', score, self.message)
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
        self.redis_endpoint = TCP4ClientEndpoint(reactor, '127.0.0.1', 6379)
        self.channel = 'heliosburn.traffic'

        self.start()

    def _subscribe(self, redis):
        self.redis_subscriber = redis
        redis.subscribe()

    def start(self, **params):
        handler_factory = HBRedisMessageHandlerFactory(TrafficHandler)
        d = self.redis_endpoint.connect(HBRedisSubscriberFactory(self.channel,
                                        handler_factory))

        d.addCallback(self._subscribe)

    def stop(self, **params):
        if self.redis_subscriber:
            self.redis_subscriber.unsubscribe()


traffic_stream = TrafficStream()

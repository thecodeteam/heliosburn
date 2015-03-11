import pymongo
from module import AbstractModule
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor
from redis_subscriber import HBRedisSubscriberFactory
from redis_subscriber import HBRedisMessageHandlerFactory
from redis_subscriber import HBRedisMessageHandler


class RequestTrafficHandler(HBRedisMessageHandler):

    def execute(self):
        mongo = pymongo.MongoClient()
#        mongo.test.test_collection.save(dict(self.message))
        print(self.message)


class ResponseTrafficHandler(HBRedisMessageHandler):

    def execute(self):
        mongo = pymongo.MongoClient()
#        mongo.test.test_collection.save(self.message)
        print(self.message)


class TrafficRecorder(AbstractModule):

    def __init__(self):
        AbstractModule.__init__(self)
        redis_endpoint = TCP4ClientEndpoint(reactor, '127.0.0.1', 6379)

        handler_factory = HBRedisMessageHandlerFactory(RequestTrafficHandler)
        redis_req = redis_endpoint.connect(
            HBRedisSubscriberFactory('traffic.request',
                                     handler_factory))
        handler_factory = HBRedisMessageHandlerFactory(ResponseTrafficHandler)
        redis_res = redis_endpoint.connect(
            HBRedisSubscriberFactory('traffic.response',
                                     handler_factory))

        redis_req.addCallback(self._subscribe)
        redis_res.addCallback(self._subscribe)

    def _subscribe(self, redis):
        self.redis = redis
        response = self.redis.subscribe()

    def start(self):
        if self.redis:
            self.redis.subscribe()

    def stop(self):
        if self.redis:
            self.redis.unsubscribe()


traffic_recorder = TrafficRecorder()

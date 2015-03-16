import pymongo
import json
import uuid
from module import AbstractModule
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor
from redis_subscriber import HBRedisSubscriberFactory
from redis_subscriber import HBRedisMessageHandlerFactory
from redis_subscriber import HBRedisMessageHandler


class TrafficRecorderHandlerFactory(HBRedisMessageHandlerFactory):

    def get_handler(self, message):
        message = json.loads(message)
        message['recording_id'] = self.recording_id

        return self.message_handler(message)

    def set_recording_id(self, recording_id):
        self.recording_id = recording_id


class TrafficHandler(HBRedisMessageHandler):

    def execute(self):
        conn = pymongo.MongoClient()
        db = conn.proxy
        db.traffic.update({'transaction_id': self.message['transaction_id']},
                          self.message,
                          upsert=True)


class TrafficRecorder(AbstractModule):

    def __init__(self):
        AbstractModule.__init__(self)
        self.redis_endpoint = TCP4ClientEndpoint(reactor, '127.0.0.1', 6379)
        self.channel = 'heliosburn.traffic'

    def _subscribe(self, redis):
        self.redis_subscriber = redis
        redis.subscribe()

    def start(self, **params):
        handler_factory = TrafficRecorderHandlerFactory(TrafficHandler)
        handler_factory.set_recording_id(params['recording_id'])
        d = self.redis_endpoint.connect(HBRedisSubscriberFactory(self.channel,
                                        handler_factory))

        d.addCallback(self._subscribe)

    def stop(self, **params):
        if self.redis_subscriber:
            self.redis_subscriber.unsubscribe()


traffic_recorder = TrafficRecorder()

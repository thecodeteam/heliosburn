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

    def __init__(self, recording_id, message_handler=None):
        HBRedisMessageHandlerFactory.__init__(self, message_handler)
        self.recording_id = recording_id

    def get_handler(self, message):
        message = json.loads(message)
        recording = {}
        recording['_id'] = self.recording_id
        recording['traffic'] = {'recording': dict(message)}

        return self.message_handler(recording)

    def set_recording_id(self, recording_id):
        self.recording_id = recording_id


class TrafficHandler(HBRedisMessageHandler):

    def execute(self):
        conn = pymongo.MongoClient()
        db = conn.proxy
        db.traffic.update({'_id': self.message['_id']},
                          {"$push": self.message['traffic']},
                          upsert=True)


class TrafficRecorder(AbstractModule):

    def __init__(self):
        AbstractModule.__init__(self)
        redis_endpoint = TCP4ClientEndpoint(reactor, '127.0.0.1', 6379)
        recording_id = uuid.uuid1()

        self.handler_factory = TrafficRecorderHandlerFactory(recording_id,
                                                             TrafficHandler)
        redis = redis_endpoint.connect(
            HBRedisSubscriberFactory('heliosburn.traffic',
                                     self.handler_factory))

        redis.addCallback(self._subscribe)

    def _subscribe(self, redis):
        self.redis = redis
        response = self.redis.subscribe()

    def start(self):
        if self.redis:
            self.handler_factory.set_recording_id(uuid.uuid1())
            self.redis.subscribe()

    def stop(self):
        if self.redis:
            self.handler_factory.recording_id = ""
            self.redis.unsubscribe()


traffic_recorder = TrafficRecorder()

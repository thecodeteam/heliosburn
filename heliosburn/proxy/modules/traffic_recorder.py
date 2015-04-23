import pymongo
import json
import uuid
import datetime
from module import AbstractModule
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor
from twisted.python import log
from protocols.redis import HBRedisSubscriberFactory
from protocols.redis import HBRedisMessageHandlerFactory
from protocols.redis import HBRedisMessageHandler


class TrafficRecorderHandlerFactory(HBRedisMessageHandlerFactory):

    def get_handler(self, message, **configs):
        self.configs = configs
        message = json.loads(message)
        message['recording_id'] = self.recording_id

        return self.message_handler(message, configs)

    def set_recording_id(self, recording_id):
        self.recording_id = recording_id


class TrafficHandler(HBRedisMessageHandler):

    def execute(self):
        conn = pymongo.MongoClient()
        db = conn.proxy
        db.traffic.update({'transaction_id': self.message['transaction_id']},
                          self.message,
                          upsert=True)
        log.msg("traffic recorded: " + self.message)


class TrafficRecorder(AbstractModule):

    def __init__(self):
        AbstractModule.__init__(self)

    def _subscribe(self, redis):
        self.redis_subscriber = redis
        redis.subscribe()

    def configure(self, **configs):
        self.configs = configs
        self.redis_host = configs['redis_host']
        self.redis_port = configs['redis_port']
        self.redis_sub_queue = configs['redis_sub_queue']

    def start(self, **params):
        handler_factory = TrafficRecorderHandlerFactory(TrafficHandler)
        handler_factory.set_recording_id(params['recording_id'])
        self.redis_endpoint = TCP4ClientEndpoint(reactor,
                                                 self.redis_host,
                                                 self.redis_port)
        self.channel = self.redis_sub_queue
        d = self.redis_endpoint.connect(HBRedisSubscriberFactory(self.channel,
                                        handler_factory))

        d.addCallback(self._subscribe)
        self.state = "running"
        self.status = datetime.datetime.now()

    def stop(self, **params):
        try:
            if self.redis_subscriber:
                self.redis_subscriber.unsubscribe()
            self.state = "stopped"
            self.status = datetime.datetime.now()
        except AttributeError:
            return "not subscribed"


traffic_recorder = TrafficRecorder()

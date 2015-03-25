from module import AbstractModule
from twisted.python import log
import json
import redis
from twisted.trial import unittest
from controller import OperationResponse
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import defer
from twisted.internet import reactor
from redis_subscriber import HBRedisSubscriberFactory
from redis_subscriber import HBRedisTestMessageHandlerFactory
from redis_subscriber import HBRedisTestMessageHandler


class TestProxyAPI(AbstractModule, unittest.TestCase):
    """
    Extension of AbstractModule used to teset the proxy controller
    API.
    """

    def _get_operation_message(self, operation, param, key):

        message = {}
        message['operation'] = operation
        message['param'] = param
        message['key'] = key

        return message

    def configure(self, **configs):
        self.redis_host = configs['redis_host']
        self.redis_port = configs['redis_port']
        self.redis_db = configs['redis_db']
        self.redis_pub_queue = configs['redis_pub_queue']
        self.redis_sub_queue = configs['redis_sub_queue']
        self.redis_client = redis.StrictRedis(host=self.redis_host,
                                              port=self.redis_port,
                                              db=self.redis_db)

    def _subscribe(self, redis):
        self.redis_subscriber = redis
        return redis.subscribe()

    def start(self):
        handler_factory = HBRedisTestMessageHandlerFactory(self._test_response,
                                                           self._test_failed)

        self.redis_endpoint = TCP4ClientEndpoint(reactor,
                                                 self.redis_host,
                                                 self.redis_port)
        self.channel = self.redis_sub_queue
        d = self.redis_endpoint.connect(HBRedisSubscriberFactory(self.channel,
                                        handler_factory))

        d.addCallback(self._subscribe).addCallback(self._publish_message)

        return handler_factory.get_deferred()

    def _test_response(self, response):
        print(self.assertEqual("200", response))
        print("test succeeded")

    def _test_failed(self, failure):
        print("test failed")

    def _publish_message(self, result):
        recording_id = {'recording_id': 1}
        message = self._get_operation_message('start_recording',
                                              recording_id,
                                              'sr_test')
        self.redis_client.publish(self.redis_pub_queue,
                                  json.dumps(message))
        return result


test_proxy_api = TestProxyAPI()

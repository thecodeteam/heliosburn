from module import AbstractModule
from twisted.python import log
import json
import redis
from twisted.trial import unittest
from controller import OperationResponse


class TestProxyAPI(AbstractModule, unittest.TestCase):
    """
    Extension of AbstractModule class used to serialize traffic
    to a Redis pubsub channel.
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
        self.redis_client = redis.StrictRedis(host=self.redis_host,
                                              port=self.redis_port,
                                              db=self.redis_db)

    def run_tests(self):
        self.test_start_recording()

    def test_start_recording(self):
        recording_id = {'recording_id': 1}
        message = self._get_operation_message('start_recording',
                                              recording_id,
                                              'sr_test')

        self.redis_client.publish(self.redis_pub_queue, json.dumps(message))
        response = self.redis_client.get('sr_test')
        self.assertEqual(response, "20")

test_proxy_api = TestProxyAPI()

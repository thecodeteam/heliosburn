from module import AbstractModule
from twisted.python import log
import time
import json
import redis
import datetime


class TrafficReader(AbstractModule):
    """
    Extension of AbstractModule class used to serialize traffic
    to a Redis pubsub channel.
    """

    def _get_request_message(self, http_message):

        request_headers = {k: v for (k, v) in http_message.requestHeaders.
                           getAllRawHeaders()}

        message = {}
        message['createdAt'] = http_message.createdAt
        message['clientProtocol'] = http_message.clientproto
        message['method'] = http_message.method
        message['uri'] = http_message.uri
        message['path'] = http_message.path
        message['args'] = http_message.args
        message['headers'] = request_headers

        return message

    def _get_response_message(self, http_message):
        response_headers = {k: v for (k, v) in http_message.responseHeaders.
                            getAllRawHeaders()}

        message = {}
        message['createdAt'] = http_message.response_createdAt
        message['clientProtocol'] = http_message.clientproto
        message['statusCode'] = http_message.code
        message['statusDescription'] = http_message.code_message
        message['headers'] = response_headers

        return message

    def _get_traffic_message(self, http_message):
        message = {}
        message['transaction_id'] = str(http_message.transaction_id)
        message['request_id'] = str(http_message.request_id)
        message['response_id'] = str(http_message.response_id)

        return message

    def configure(self, **configs):
        self.redis_host = configs['redis_host']
        self.redis_port = configs['redis_port']
        self.redis_db = configs['redis_db']
        self.redis_pub_queue = configs['redis_pub_queue']
        self.redis_client = redis.StrictRedis(host=self.redis_host,
                                              port=self.redis_port,
                                              db=self.redis_db)

    def handle_request(self, request):

        message = self._get_traffic_message(request)
        message['request'] = self._get_request_message(request)

        self.redis_client.publish(self.redis_pub_queue, json.dumps(message))
        log.msg("traffic read: " + str(message))
        return request

    def handle_response(self, response):

        message = self._get_traffic_message(response)
        message['request'] = self._get_request_message(response)
        message['response'] = self._get_response_message(response)

        self.redis_client.publish(self.redis_pub_queue, json.dumps(message))
        log.msg("traffic read: " + str(message))
        return response

traffic_reader = TrafficReader()

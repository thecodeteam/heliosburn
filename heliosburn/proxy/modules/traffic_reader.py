from module import AbstractModule
from twisted.python import log
import time
import json
import redis
import datetime


class TrafficReader(AbstractModule):
    """
    Extension of AbstractModule class used to serialize items to Redis.
    """

    def handle_request(self, request):

        log.msg("TrafficeReader started handling of request: %s" % request)
        r = redis.StrictRedis(host='127.0.0.1',
                              port=6379,
                              db=0)

        r.publish('traffic.request', request)

        return request

    def handle_response(self, response):

#        log.msg("TrafficeReader started handling of response: %s" % response)
        r = redis.StrictRedis(host='127.0.0.1',
                              port=6379,
                              db=0)

        r.publish('traffic.response', response)
        return response

traffic_reader = TrafficReader()

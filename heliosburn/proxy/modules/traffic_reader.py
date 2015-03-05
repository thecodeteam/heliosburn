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

    def handle_request(self, request, **kwargs):

        log.msg("TrafficeReader started handling of request: %s" % request)
        return request

    def handle_response(self, response, **kwargs):

        return response

traffic_reader = TrafficReader()

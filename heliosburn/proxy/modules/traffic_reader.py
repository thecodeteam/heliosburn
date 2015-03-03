from module import AbstractModule
import time
import json
import redis
import datetime


class TrafficReader(AbstractModule):
    """
    Extension of AbstractModule class used to serialize items to Redis.
    """

    def handle_request(self, request, **kwargs):

        return request

    def handle_response(self, response, **kwargs):

        return response

traffic_reader = TrafficReader()

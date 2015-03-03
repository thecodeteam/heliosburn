from module import AbstractModule
import time
import json
import redis
import datetime


class TrafficRecorder(AbstractModule):

    def subscribe(self):
        pass

    def unsbuscribe(self):
        pass

    def record(self):
        pass


traffic_recorder = TrafficRecorder()

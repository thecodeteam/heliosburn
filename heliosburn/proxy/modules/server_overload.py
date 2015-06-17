import datetime
import pymongo
import random
import time
from injectors import ExponentialInjector
from injectors import PlateauInjector
from module import AbstractModule
from twisted.python import log


test_so_profile = {
    "_id": "0xdeadbeef",
    "name": "Raspberry PI Overload profile",
    "description": "bla bla...",
    "function": {
        "type": "exponential",
        "expValue": "3",
        "growthRate": "3"
    },
    "response_triggers": [
        {
            "fromLoad": 70,
            "toLoad": 80,
            "actions": [
                {
                    "type": "response",
                    "value": "503",
                    "percentage": 30
                },
                {
                    "type": "delay",
                    "value": "300",
                    "percentage": 100
                }
            ]
        },
        {
            "fromLoad": 80,
            "toLoad": 100,
            "actions": [
                {
                    "type": "response",
                    "value": "503",
                    "percentage": 100
                }
            ]
        }
    ]
}


class ResponseTrigger(object):

    def __init__(self, min_load, max_load, probability):
        self.min_load = min_load
        self.max_load = max_load
        self.probability = probability

    def match(self, load):
        matched = False
        if load >= self.min_load and load <= self.max_load:
            if random.random() <= self.probability/100:
                matched = True

        return matched

    def get_response(self):
        pass


class SimulatedResponseTrigger(ResponseTrigger):

    def __init__(self, min_load, max_load, probability, response):
        ResponseTrigger.__init(self, min_load, max_load, probability)
        self.response = response

    def get_response(self):
        return self.response


class DelayedResponseTrigger(ResponseTrigger):

    def __init__(self, min_load, max_load, probability, delay):
        ResponseTrigger.__init(self, min_load, max_load, probability)
        self.delay = delay

    def get_response(self):
        time.sleep(self.delay)
        return None


class ServerOverload(AbstractModule):
    injectors = {
        'exponential': ExponentialInjector,
        'plateau': PlateauInjector
    }
    triggers = []

    def __init__(self):
        AbstractModule.__init__(self)
        self.redis_host = '127.0.0.1'
        self.redis_port = 6379
        self.redis_db = 0
        self.mongo_host = 'heliosburn.traffic'
        self.mongo_port = '127.0.0.1'
        self.mongo_db = 'heliosburn'

    def configure(self, **configs):
        pass

    def handle_request(self, request):
        for injector in self.injectors:
            load = injector(request, self.profile).execute()

        for trigger in self.triggers:
            if trigger.match(load):
                response = trigger.get_response()

            if response:
                pass
                # add in automatically responding with response code
            else:
                return request

    def _set_profile(self, profile_id):
        conn = pymongo.MongoClient()
        db = conn.proxy
        profile = db.so_profile.find_one({"_id": profile_id})
        profile = test_so_profile
        self.profile = profile

    def _set_triggers(self):
        for trigger in self.profile['response_triggers']:
            min_load = trigger['fromLoad']
            max_load = trigger['toLoad']
            for action in trigger['actions']:
                if action['type'] == "response":
                    response = action['value']
                    prob = action['percentage']
                    sr_trigger = SimulatedResponseTrigger(min_load,
                                                          max_load,
                                                          prob,
                                                          response
                                                          )

                    self.triggers.append(sr_trigger)

                if action['type'] == "delay":
                    response = action['value']
                    prob = action['percentage']
                    d_trigger = DelayedResponseTrigger(min_load,
                                                       max_load,
                                                       prob,
                                                       response
                                                       )
                    self.triggers.append(d_trigger)

    def start(self, **params):
        profile_id = params['profile_id']
        self.state = "running"
        self.status = str(datetime.datetime.now())
        self._set_profile(profile_id)
        log.msg("Server Overload module started at: " + self.status)

    def stop(self, **params):
        self.state = "stopped"
        self.profile = None
        self.status = str(datetime.datetime.now())
        log.msg("Server Overload module stopped at: " + self.status)

so = ServerOverload()

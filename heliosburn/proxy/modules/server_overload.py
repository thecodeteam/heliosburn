import datetime
import pymongo
import math
from module import AbstractModule
from twisted.python import log


test_session = {
        "id": 1,
        "name": "Session A",
        "description": "This is a description for a Session",
        "upstreamHost": "github.com",
        "upstreamPort": 80,
        "qosProfile": "0xdeadbeef",
        "ServerOverloadProfile": "0xfedbeef",

        "createdAt": "2014-02-12 03:34:51",
        "updatedAt": "2014-02-12 03:34:51",
        "testPlan": {
                "id": 12,
                "name": "ViPR Test plan"
            },
        "user": {
                "id": 1,
                "username": "John Doe"
            },
        "executions": 42,
        "latest_execution_at": "2014-02-12 03:34:51"
    }

test_profile = {
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


class SOInjector(object):

    def __init__(self, request, so_profile):
        self.request = request
        self.so_profile = so_profile

    def execute(self):
        pass


class ExponentialInjector(SOInjector):

    load = 1
    requests = 0

    def execute(self):
        x = self.so_profile['function']['expValue']
        r = self.so_profile['function']['growthRate']
        self.f = self.so_profile['function']['fluxuation']
        maxL = self.so_profile['function']['maxLoad']

        if self.load < 100 and self.load < maxL:
            if self.requests < r:
                self.requests + 1

            if self.requests == r:
                self.load = (self.load * x) + math.sin(self.f)
                self.requests = 0
                if self.load > 100:
                    self.load = 100

        return self.load


class PlateauInjector(SOInjector):
    load = 1
    requests = 0

    def execute(self):
        self.requests = self.so_profile['function']['requestStart']
        x = self.so_profile['function']['growthAmount']
        r = self.so_profile['function']['growthRate']
        self.f = self.so_profile['function']['fluxuation']

        if self.load < 100:
            if self.requests < r:
                self.requests + 1

            if self.requests == r:
                self.load = (self.load * x) + math.sin(self.f)
                self.requests = 0
                if self.load > 100:
                    self.load = 100


class NullInjector(SOInjector):
    def execute(self):
        if self.request:
            return self.request
        else:
            return self.response


class ServerOverload(AbstractModule):
    injectors = {
        'exponential': ExponentialInjector,
        'plateau': PlateauInjector
    }

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
            request = injector(request, self.so_profile).execute()

        return request

    def _get_session(self, session_id):
        conn = pymongo.MongoClient()
        db = conn.proxy
        session = db.session.find_one({"_id": session_id})
        session = test_session
        return session

    def _set_profile(self, session_id):
        session = self._get_session(session_id)
        profile_id = session["serverOverloadProfile"]
        conn = pymongo.MongoClient()
        db = conn.proxy
        profile = db.so_profile.find_one({"_id": profile_id})
        profile = test_profile
        self.so_profile = profile

    def start(self, **params):
        session_id = params['session_id']
        self.state = "running"
        self.status = str(datetime.datetime.now())
        self._set_profile(session_id)
        log.msg("Server Overload module started at: " + self.status)

    def stop(self, **params):
        self.state = "stopped"
        self.status = str(datetime.datetime.now())
        log.msg("Server Overload module stopped at: " + self.status)

so = ServerOverload()

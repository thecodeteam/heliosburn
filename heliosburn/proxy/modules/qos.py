import time
import random
import datetime
from module import AbstractModule
from twisted.python import log

test_profile = {
    "createdAt": "2014-02-12 03:34:51",
    "updatedAt": "2014-02-12 03:34:51",
    "latency": 100,
    "jitter": {
        "min": 30,
        "max": 50
    },
    "trafficLoss": 0.1
}

test_session = {
    "id": 1,
    "name": "Session A",
    "description": "This is a description for a Session",
    "upstreamHost": "github.com",
    "upstreamPort": 80,
    "createdAt": "2014-02-12 03:34:51",
    "updatedAt": "2014-02-12 03:34:51",
    "testPlan":
    {
        "id": 12,
        "name": "ViPR Test plan"
    },
    "qos":
    {
        "id": 45
    },
    "serverOverload":
    {
        "id": 951
    },
    "user":
    {
        "id": 1,
        "username": "John Doe"
    },
    "executions": 42,
}


class QOSAction(object):

    def __init__(self, action_dict, request=None, response=None):
        self.action_dict = action_dict
        self.request = request
        self.response = response

    def execute(self):
        pass


class LatencyAction(QOSAction):

    def __init__(self,
                 action_dict,
                 request=None,
                 response=None,
                 minimum=None,
                 maximum=None):

        QOSAction.__init__(self, action_dict, request, response)

        if minimum:
            self.minimum = minimum
        if maximum:
            self.maximum = maximum

    def execute(self):
        lagtime = None

        if 0 < self.minimum < self.maximum:
            lagtime = random.randrange(self.minimum, self.maximum)

        if lagtime is not None:
            log.msg("sleeping for: %s (%s, %s)" % (lagtime,
                                                   self.minimum,
                                                   self.maximum))
            time.sleep(lagtime)

        if self.request:
            return self.request
        else:
            return self.response


class JitterAction(QOSAction):

    def execute(self):
        pass


class PacketLossAction(QOSAction):

    def execute(self):
        pass


class NullAction(QOSAction):
    def execute(self):
        if self.request:
            return self.request
        else:
            return self.response


class QOS(AbstractModule):
    actions = {
        'latency': LatencyAction,
        'jitter': JitterAction,
        'packet_loss': PacketLossAction,
        'null': NullAction
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

    def handle_request(self, request, minimum=1, maximum=1):

        return request

    def handle_response(self, response, minimum=1, maximum=1):
        pass

    def start(self, **params):
        self.session_id = params['session_id']
        self.state = "running"
        self.status = str(datetime.datetime.now())
        log.msg("QOS module started at: " + self.status)

    def stop(self, **params):
        self.injection_engine = None
        self.state = "stopped"
        self.status = str(datetime.datetime.now())
        log.msg("QOS module stopped at: " + self.status)

qos = QOS()

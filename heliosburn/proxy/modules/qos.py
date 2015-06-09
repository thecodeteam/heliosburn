import time
import random
import datetime
from module import AbstractModule
from twisted.python import log
from threading import Lock

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


class QOSInjector(object):

    def __init__(self, request, qos_profile):
        self.request = request
        self.qos_profile = qos_profile

    def execute(self):
        pass


class LatencyInjector(QOSInjector):

    def execute(self):
        lagtime = 0
        latency = self.qos_profile['latency']
        minimum = self.qos_profile['jitter']['minimum']
        maximum = self.qos_profile['jitter']['maximum']

        if 0 < minimum < maximum:
            lagtime = random.randrange(latency + self.minimum,
                                       latency + self.maximum)

        if lagtime is not None:
            log.msg("sleeping for: %s (%s, %s)" % (lagtime,
                                                   self.minimum,
                                                   self.maximum))
            time.sleep(lagtime)

        return self.request


class PacketLossInjector(QOSInjector):

    _mutex = Lock()
    _packets = 0
    _requests_dropped = 0

    def execute(self):

        self._mutex.aquire()

        self._packets += 1
        traffic_loss = self.qos_profile["trafficloss"]
        return_value = self.request

        if self._packets_dropped/self._packets < traffic_loss:
            self._requests_dropped += 1
            return_value = False

        self._mutex.release()

        return return_value


class QOS(AbstractModule):
    actions = {
        'latency': LatencyInjector,
        'packet_loss': PacketLossInjector,
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

        return request

    def _get_session(self, session_id):
        # get from mongo here
        return test_session

    def _set_profile(self, session_id):
        session = self._get_session(session_id)
        session["qosProfile"]
        # get from mongo here
        self.qos_profile = test_profile

    def start(self, **params):
        session_id = params['session_id']
        self.state = "running"
        self.status = str(datetime.datetime.now())
        self._set_profile(session_id)
        log.msg("QOS module started at: " + self.status)

    def stop(self, **params):
        self.state = "stopped"
        self.status = str(datetime.datetime.now())
        log.msg("QOS module stopped at: " + self.status)

qos = QOS()

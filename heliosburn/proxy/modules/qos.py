import datetime
import pymongo
from injectors import LatencyInjector
from injectors import PacketLossInjector
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


class QOS(AbstractModule):
    injectors = {
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
        for injector in self.injectors:
            request = injector(request, self.qos_profile).execute()

# might be a problem upstream if no request is returned
        if request:
            return request

    def _set_profile(self, session_id):
        session = self.get_session(session_id)
        profile_id = session["qosProfile"]
        conn = pymongo.MongoClient()
        db = conn.proxy
        profile = db.qos_profile.find_one({"_id": profile_id})
        profile = test_profile
        self.qos_profile = profile

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

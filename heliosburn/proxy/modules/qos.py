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

# ultimately pull from settings file
injector_list = [
    LatencyInjector,
    PacketLossInjector
]


class QOS(AbstractModule):
    injectors = []

    def __init__(self):
        AbstractModule.__init__(self)
        self.redis_host = '127.0.0.1'
        self.redis_port = 6379
        self.redis_db = 0
        self.mongo_host = 'heliosburn.traffic'
        self.mongo_port = '127.0.0.1'
        self.mongo_db = 'heliosburn'
        self.stats['qos'] = []

    def configure(self, **configs):
        pass

    def handle_request(self, request):
        for injector in self.injectors:
            request = injector.execute()
            self.stats['QOS'].append(injector.metrics)

# might be a problem upstream if no request is returned
        if request:
            return request

    def _set_profile(self, profile_id):
        conn = pymongo.MongoClient()
        db = conn.proxy
        profile = db.qos_profile.find_one({"_id": profile_id})
        profile = test_profile
        self.profile = profile

    def start(self, **params):
        self.session_id = params['session_id']
        self.profile_id = params['profile_id']
        self.state = "running"
        self.status = str(datetime.datetime.now())
        self._set_profile(self.profile_id)
        for c in injector_list:
            self.injectors.append(c(self.profile))
        log.msg("QOS module started at: " + self.status)

    def stop(self, **params):
        self.state = "stopped"
        self.status = str(datetime.datetime.now())
        self.injectors = []
        log.msg("QOS module stopped at: " + self.status)

qos = QOS()

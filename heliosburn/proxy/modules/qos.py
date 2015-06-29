import datetime
from injectors import LatencyInjector
from injectors import PacketLossInjector
from module import AbstractModule
from twisted.python import log
from module_decorators import SkipHandler
from models import QOSProfileModel

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
        self.stats['QOS'] = []

    def configure(self, **configs):
        pass

    @SkipHandler
    def handle_request(self, request):
        for injector in self.injectors:
            injector.execute()
            request.delay += injector.delay
            drop_request = injector.drop_request
            self.stats['QOS'].append(injector.metrics)

        if drop_request:
            return None
        else:
            log.msg("Returning QOS request: " + str(request))
            return request

    def start(self, **params):
        self.session_id = params['session_id']
        self.profile_id = params['profile_id']
        self.profile = QOSProfileModel({"_id": self.profile_id})
        self.state = "running"
        self.status = str(datetime.datetime.now())
        for c in injector_list:
            self.injectors.append(c(self.profile))
        log.msg("QOS module started at: " + self.status)

    def stop(self, **params):
        self.state = "stopped"
        self.status = str(datetime.datetime.now())
        self.injectors = []
        log.msg("QOS module stopped at: " + self.status)

qos = QOS()

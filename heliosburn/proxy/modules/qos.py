import time
import random
import datetime
from module import AbstractModule
from twisted.python import log
from traffic_eval.traffic_evaluator import TrafficEvaluator


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

    def configure(self, **configs):
        self.redis_host = configs['redis_host']
        self.redis_port = configs['redis_port']
        self.redis_db = configs['redis_db']
        self.mongo_host = configs['mongo_host']
        self.mongo_port = configs['mongo_port']
        self.mongo_db = configs['mongo_db']

    def _get_config(self):
        config = {
            "config": {
                "redis": {
                    "db": self.redis_db,
                    "port": self.redis_port,
                    "host": self.redis_host
                },
                "mongodb": {
                    "host": self.mongo_host,
                    "db": {
                        "production": self.mongo_db,
                        "test": "heliosburn_test"
                    },
                    "port": self.mongo_port
                }
            }
        }

        return config

    def _process_request(self, http_metadata, session):
        log.msg("calling traffic evaluator with:\n" +
                "http_metadata: " + str(http_metadata) + "\n"
                "      session: " + str(session))
        action = self.injection_engine.get_action(http_metadata, session)

        return action

    def _process_response(self, http_metadata, session):
        log.msg("calling traffic evaluator with:\n" +
                "http_metadata: " + str(http_metadata) + "\n"
                "      session: " + str(session))
        action = self.injection_engine.get_action(http_metadata, session)

        return action

    def handle_request(self, request, minimum=1, maximum=1):

        return request

    def handle_response(self, response, minimum=1, maximum=1):
        pass

    def start(self, **params):
        self.injection_engine = TrafficEvaluator(self._get_config())
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

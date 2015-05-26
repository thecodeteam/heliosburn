import datetime
from module import AbstractModule
from twisted.python import log
from traffic_eval.traffic_evaluator import TrafficEvaluator


class SOAction(object):

    def __init__(self, action_dict, request=None, response=None):
        self.action_dict = action_dict
        self.request = request
        self.response = response

    def execute(self):
        pass


class ExpOverloadAction(SOAction):

    def execute(self):
        pass


class DoSAction(SOAction):

    def execute(self):
        pass


class NullAction(SOAction):
    def execute(self):
        if self.request:
            return self.request
        else:
            return self.response


class ServerOverload(AbstractModule):
    actions = {
        'ExpOverload': ExpOverloadAction,
        'DoS': DoSAction,
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
        log.msg("Server Overload module started at: " + self.status)

    def stop(self, **params):
        self.injection_engine = None
        self.state = "stopped"
        self.status = str(datetime.datetime.now())
        log.msg("Server Overload module stopped at: " + self.status)

so = ServerOverload()

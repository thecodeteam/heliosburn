import datetime
import random
from injectors import ExponentialInjector
from injectors import PlateauInjector
from module import AbstractModule
from twisted.python import log
from module_decorators import SkipHandler
from models import SOProfileModel


# ultimately pull from settings file
injector_map = {
    "exponential": ExponentialInjector,
    "plateau": PlateauInjector
}


class ResponseTrigger(object):

    def __init__(self, min_load, max_load, probability):
        self.min_load = min_load
        self.max_load = max_load
        self.probability = probability
        self.metrics = {}
        self.delay = 0

    def match(self, load):
        matched = False
        if load >= self.min_load and load <= self.max_load:
            if random.random() <= self.probability/100:
                matched = True
        if matched:
            self.metrics[self.__class__.__name__] += 1

        return matched

    def get_response(self):
        pass


class SimulatedResponseTrigger(ResponseTrigger):

    def __init__(self, min_load, max_load, probability, response):
        ResponseTrigger.__init__(self, min_load, max_load, probability)
        self.response = response

    def get_response(self):
        return self.response


class DelayedResponseTrigger(ResponseTrigger):

    def __init__(self, min_load, max_load, probability, delay):
        ResponseTrigger.__init__(self, min_load, max_load, probability)
        self.delay = delay

    def get_response(self):
        return None


class ServerOverload(AbstractModule):
    triggers = []
    injectors = []
    response = None

    def __init__(self):
        AbstractModule.__init__(self)
        self.redis_host = '127.0.0.1'
        self.redis_port = 6379
        self.redis_db = 0
        self.mongo_host = 'heliosburn.traffic'
        self.mongo_port = '127.0.0.1'
        self.mongo_db = 'heliosburn'
        self.stats['ServerOverload'] = []
        self.response_code = None

    def configure(self, **configs):
        pass

    @SkipHandler
    def handle_request(self, request):
        for injector in self.injectors:
            load = injector.execute()
            log.msg("Load:" + str(load))
            self.stats['ServerOverload'].append(injector.metrics)

        log.msg("about to trigger:")
        for trigger in self.triggers:
            log.msg("checking triggers:")
            if trigger.match(load):
                self.stats['ServerOverload'].append(trigger.metrics)
                self.response_code = trigger.get_response()
                request.delay += trigger.delay

        log.msg("ServerOverload request: " + str(request))

        return request

    @SkipHandler
    def handle_response(self, response):
        if self.response_code:
            response.code = self.response_code

        return response

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
        self.session_id = params['session_id']
        self.profile_id = params['profile_id']
        self.profile = SOProfileModel(self.profile_id)
        self.state = "running"
        self.status = str(datetime.datetime.now())
        self._set_triggers()
        injector_type = self.profile['function']['type']
        self.injectors.append(injector_map[injector_type](self.profile))

        log.msg("Server Overload module started at: " + self.status)

    def stop(self, **params):
        self.state = "stopped"
        self.profile = None
        self.status = str(datetime.datetime.now())
        self.injectors = []
        log.msg("Server Overload module stopped at: " + self.status)

so = ServerOverload()

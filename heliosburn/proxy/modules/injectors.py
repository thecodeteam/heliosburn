
import math
import time
import random
from twisted.python import log


class Injector(object):

    metrics = {}

    def __init__(self, profile):
        self.profile = profile

    def execute(self, request):
        pass


class NullInjector(Injector):
    def execute(self):
        pass


class ExponentialInjector(Injector):

    load = 1
    requests = 0

    def execute(self):
        x = self.profile['function']['expValue']
        r = self.profile['function']['growthRate']
        self.f = self.profile['function']['fluxuation']
        maxL = self.profile['function']['maxLoad']

        if self.load < 100 and self.load < maxL:
            if self.requests < r:
                self.requests + 1

            if self.requests == r:
                self.load = (self.load * x) + math.sin(self.f)
                self.requests = 0
                if self.load > 100:
                    self.load = 100

        self.metrics['load'] = self.load
        self.metrics['requests'] = self.requests

        return self.load


class PlateauInjector(Injector):
    load = 1
    requests = 0

    def execute(self):
        self.requests = self.profile['function']['requestStart']
        x = self.profile['function']['growthAmount']
        r = self.profile['function']['growthRate']
        self.f = self.profile['function']['flucuation']

        if self.load < 100:
            if self.requests < r:
                self.requests + 1

            if self.requests == r:
                self.load = (self.load * x) + math.sin(self.f)
                self.requests = 0
                if self.load > 100:
                    self.load = 100

        self.metrics['load'] = self.load
        self.metrics['requests'] = self.requests

        return self.load


class LatencyInjector(Injector):

    def execute(self):
        lagtime = 0
        latency = self.profile['latency']
        minimum = self.profile['jitter']['min']
        maximum = self.profile['jitter']['max']

        if 0 < minimum < maximum:
            lagtime = random.randrange(latency + minimum,
                                       latency + maximum)

        if lagtime is not None:
            log.msg("sleeping for: %s (%s, %s)" % (lagtime,
                                                   minimum,
                                                   maximum))
            time.sleep(lagtime)

        self.metrics['lagtime'] = lagtime


class PacketLossInjector(Injector):

    _requests = 0
    _requests_dropped = 0

    def execute(self):

        self._requests += 1
        traffic_loss = self.profile["trafficLoss"]
        return_value = True

        if self._requests_dropped/self._requests < traffic_loss:
            self._requests_dropped += 1
            return_value = False

        self.metrics['requests'] = self._requests
        self.metrics['dropped_requests'] = self._requests_dropped

        return return_value

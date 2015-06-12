
import math
import time
import random
from twisted.python import log
from threading import Lock


class Injector(object):

    def __init__(self, request, profile):
        self.request = request
        self.profile = profile

    def execute(self):
        pass


class NullInjector(Injector):
    def execute(self):
        if self.request:
            return self.request


class ExponentialInjector(Injector):

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


class PlateauInjector(Injector):
    load = 1
    requests = 0

    def execute(self):
        self.requests = self.so_profile['function']['requestStart']
        x = self.so_profile['function']['growthAmount']
        r = self.so_profile['function']['growthRate']
        self.f = self.so_profile['function']['flucuation']

        if self.load < 100:
            if self.requests < r:
                self.requests + 1

            if self.requests == r:
                self.load = (self.load * x) + math.sin(self.f)
                self.requests = 0
                if self.load > 100:
                    self.load = 100

        return self.load


class LatencyInjector(Injector):

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


class PacketLossInjector(Injector):

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

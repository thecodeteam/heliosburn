
import random
from twisted.python import log


class Injector(object):

    def __init__(self, profile):
        self.profile = profile
        self.requests = 0
        self.requests_dropped = 0
        self.metrics = {}
        self.drop_request = False
        self.delay = 0

    def execute(self):
        pass


class LoadInjector(Injector):
    def __init__(self, profile):
        Injector.__init__(self, profile)
        self.load = 1

    def calculate_load(self):
        self.load += 1
        return self.load

    def execute(self):
        self.calculate_load()


class NullInjector(Injector):
    def execute(self):
        pass


class ExponentialInjector(LoadInjector):

    def calculate_load(self):
        '''
        Calulates an exponential load
        Return: the calulated load
        '''

        x = self.profile['function']['expValue']
        r = self.profile['function']['growthRate']
#        self.f = self.profile['function']['fluxuation']
#        maxL = self.profile['function']['maxLoad']
        self.f = 1
        maxL = 100

        if int(self.load) < 100 and int(self.load) < int(maxL):
            if int(self.requests) < int(r):
                self.requests += 1

            if int(self.requests) >= int(r):
                self.load += (int(self.load) * int(x)) + random.randrange(
                    0, int(self.f))
                self.requests = 0
                if int(self.load) > 100:
                    self.load = 100

        self.metrics['load'] = self.load
        if 'requests' in self.metrics:
            self.metrics['requests'] += self.requests
        else:
            self.metrics['requests'] = self.requests

        log.msg("Current Exponential  Metrics: " + str(self.metrics))

        return self.load


class PlateauInjector(LoadInjector):

    def execute(self):
        '''
        Calculates a load that plateau's over time
        Return: the calulated load
        '''
        self.requests = self.profile['function']['requestStart']
#        x = self.profile['function']['growthAmount']
        x = self.profile['function']['expValue']
        r = self.profile['function']['growthRate']
#        self.f = self.profile['function']['fluxuation']
        self.f = 0

        if self.load < 100:
            if self.requests < r:
                self.requests + 1

            if self.requests == r:
                self.load = self.load + x
                self.requests = 0
                if self.load > 100:
                    self.load = 100

        self.metrics['load'] = self.load
        self.metrics['requests'] = self.requests
        log.msg("Current Plateau Metrics: " + str(self.metrics))


class LatencyInjector(Injector):

    def execute(self):
        '''
        Injects latency into the request
        Return
        '''
        lagtime = 0
        latency = self.profile['latency']
        minimum = self.profile['jitter']['min']
        maximum = self.profile['jitter']['max']

        if 0 < minimum < maximum:
            lagtime = random.randrange(latency + minimum,
                                       latency + maximum)

        self.delay = lagtime
        self.metrics['lagtime'] = lagtime
        log.msg("Current Latency Metrics: " + str(self.metrics))


class PacketLossInjector(Injector):

    def execute(self):

        self.drop_request = False
        self.requests += 1
        traffic_loss = float(self.profile["trafficLoss"])
        t_percent = float(self.requests_dropped)/float(self.requests)

        if self.requests < (100 * traffic_loss):
            if random.getrandbits(1):
                self.requests_dropped += 1
                self.drop_request = True

        elif t_percent < traffic_loss:
            self.requests_dropped += 1
            self.drop_request = True

        self.metrics['requests'] = self.requests
        self.metrics['dropped_requests'] = self.requests_dropped

        if self.drop_request:
            log.msg("Packet Loss Injected, skipping processing")
            log.msg("t_percent:" + str(t_percent))
            log.msg("traffic_loss:" + str(traffic_loss))

        log.msg("Current Packet Loss Metrics: " + str(self.metrics))

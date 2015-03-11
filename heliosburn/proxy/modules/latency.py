import time
import random
from module import AbstractModule
from twisted.python import log


class Latency(AbstractModule):

    def handle_request(self, request, minimum=1, maximum=1):

        lagtime = None

#        log.msg("Latency started handling of request: %s" % request)

        if 0 < minimum < maximum:
            lagtime = random.randrange(minimum, maximum)

        if lagtime is not None:
            log.msg("sleeping for: %s (%s, %s)" % (lagtime, minimum, maximum))
            time.sleep(lagtime)

        return request

latency = Latency()

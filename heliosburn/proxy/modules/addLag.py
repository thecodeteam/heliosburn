from modules.base import ProxyModuleBase

class addLag(ProxyModuleBase):

    def onRequest(self, minimum = 1, maximum = 1, **keywords):
        import time
        import random
        lagtime = None

        if 'minimum' in keywords:
            minimum = keywords['minimum']
        if 'maximum' in keywords:
            maximum = keywords['maximum']

        if minimum > 0 and  maximum > minimum:
            lagtime = random.randrange(minimum,maximum)

        if lagtime is not None:
            print "sleeping for: %s (%s, %s)" % (lagtime, minimum, maximum)
            time.sleep(lagtime)
        else:
            print "pretend we slept here"


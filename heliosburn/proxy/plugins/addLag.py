from proxy.modules import IModule
from proxy.modules import AbstractModule
from zope.interface import implements
from twisted.plugin import IPlugin


class addLag(AbstractModule):
    implements(IPlugin, IModule)

    def get_name(self):
        self.name = "addLag"
        return self.name

    def onRequest(self, minimum=1, maximum=1, **keywords):
        import time
        import random

        lagtime = None

        if 'minimum' in keywords:
            minimum = keywords['minimum']
        if 'maximum' in keywords:
            maximum = keywords['maximum']

        if 0 < minimum < maximum:
            lagtime = random.randrange(minimum, maximum)

        if lagtime is not None:
            print "sleeping for: %s (%s, %s)" % (lagtime, minimum, maximum)
            time.sleep(lagtime)
        else:
            print "pretend we slept here"


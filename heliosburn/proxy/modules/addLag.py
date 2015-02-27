from module import AbstractModule


class addLag(AbstractModule):

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


add_lag = addLag()

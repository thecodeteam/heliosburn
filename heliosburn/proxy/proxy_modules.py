#This is a set of sample modules to serve as examples and be used in testing
#in these examples 'arguments' is a tuple parameter generated from the entries
#in config.yml. Likewise, 'keywords' is a dictionary.  

from twisted.internet import reactor, defer
from twisted.python import threadable; threadable.init(1)
import sys, time

def addLag(RequestObject, minimum = 1, maximum = 1):
    """
    This function takes a minimum (and maximum) wait time. Every request is
    subjected to an additional wait based on these parameters.

    Examples:
        addLag(RequestObject, 3, 5) -- and between 3 and 5 seconds of lag

    NOTE: This is only an example. This implementation adds a blocking wait
    (time.sleep()). 
    """
    import time
    import random

    lagtime = None
    if minimum > 0 and maximum > minimum:
        lagtime = random.randrange(minimum, maximum)

    if minimum == maximum:
        lagtime = minimum

    if lagtime is not None:
        print "sleeping for: %s (%s, %s)" % (lagtime, minimum, maximum)
        time.sleep(lagtime)
    else:
        print "pretend we slept here"

    return RequestObject
    

def makeBanner(RequestObject, message = "banner"):

    print "#################################################################"
    print message
    print "#################################################################"

    return RequestObject


def responseCode(RequestObject):

    if RequestObject.father.code == 404:
        RequestObject.father.code = 200

    return RequestObject

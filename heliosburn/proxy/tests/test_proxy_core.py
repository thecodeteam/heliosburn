from proxy.proxy_core import MyReverseProxyResource
from proxy.proxy_core import MyReverseProxyRequest
from proxy.proxy_core import MyProxyClient
from proxy.proxy_core import MyProxyClientFactory
from twisted.trial import unittest
from twisted.test import proto_helpers

class MyProxyClientTestCase(unittest.TestCase):
    def setUp(self):
        factory = MyProxyClientFactory
        self.proto = MyProxyClient
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def _test(self, operation, expected):
        #self.proto.dataReceived(
        #self.assertEqual( , expected)


class MyReverseProxyResourceTestCase(unittest.TestCase):
    def setUp(self):
        pass


class MyReverseProxyRequestTestCase(unittest.TestCase):
    def setUp(self):
        pass


def main():
    from twisted.internet import reactor
    from twisted.python import log
    import sys
    log.startLogging(sys.stdout)
    reactor.listenTCP(0

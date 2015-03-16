from heliosburn.proxy.hbproxy import HBProxyMgmtRedisSubscriberFactory
from heliosburn.proxy.hbproxy import HBProxyMgmtProtocolFactory
from heliosburn.proxy.hbproxy import HBProxy
from twisted.trial import unittest
from twisted.test import proto_helpers


class ProxyInterfaceProtocolTestCase(unittest.TestCase):

    def setUp(self):
        self.hb_proxy = HBProxy("/home/vagrant/HeliosBurn/heliosburn/"
                                + "proxy/config.yaml")
        self.hb_proxy.run()
        protoFactory = HBProxyMgmtProtocolFactory(self.hb_proxy)
        self.proto = protoFactory.buildProtocol(('127.0.0.1', 6379))
        self.proto_transport = proto_helpers.StringTransport()
        self.proto.makeConnection(self.proto_transport)

    def _test(self, operation, expected):
        self.proto.dataReceived(operation)
        self.assertEqual(self.proto_transport.value(), expected)

    def test_stop(self):
        operation = "stop"
        expected = "stop"

        return self._test(operation, expected)

    def test_start(self):
        operation = "start"
        expected = "start"

        return self._test(operation, expected)

    def test_reset(self):
        operation = "reset"
        expected = "reset"

        return self._test(operation, expected)

    def test_reload(self):
        operation = "reload"
        expected = "reload"

        return self._test(operation, expected)

    def test_change_upstream_host(self):
        operation = "upstream_host 192.168.1.1"
        expected = "upstream_host 192.168.1.1"

        return self._test(operation, expected)

    def test_change_upstream_port(self):
        operation = "upstream_port 8900"
        expected = "upstream_port 8900"

        return self._test(operation, expected)

    def test_change_listen_address(self):
        operation = "listen_address 192.168.1.2"
        expected = "listen_address  192.168.1.2"

        return self._test(operation, expected)

    def test_change_listen_port(self):
        operation = "listen_port 8989"
        expected = "listen_port  8989"

        return self._test(operation, expected)


class ProxyInterfaceRedisTestCase(ProxyInterfaceProtocolTestCase):

    def setUp(self):
        self.hb_proxy = HBProxy("/home/vagrant/HeliosBurn/heliosburn/"
                                + "proxy/config.yaml")
        self.hb_proxy.run()
        protoFactory = HBProxyMgmtRedisSubscriberFactory(self.hb_proxy)
        self.proto = protoFactory.buildProtocol(('127.0.0.1', 6379))
        self.proto_transport = proto_helpers.StringTransport()
        self.proto.makeConnection(self.proto_transport)


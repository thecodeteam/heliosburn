import yaml
import os
from protocols import HBProxyMgmtRedisSubscriberFactory
from protocols import HBProxyMgmtProtocolFactory
from controller import HBProxyController
from controller import OperationFactory
from twisted.trial import unittest
from twisted.test import proto_helpers


def get_op_factory():
    config = get_config("../config.yaml")
    plugins = get_config("../modules.yaml")
    proxy_config = config['proxy']
    mgmt_config = config['mgmt']
    bind_address = proxy_config['bind_address']
    protocols = proxy_config['protocols']
    upstream_host = proxy_config['upstream']['address']
    upstream_port = proxy_config['upstream']['port']
    tcp_mgmt_address = mgmt_config['tcp']['address']
    tcp_mgmt_port = mgmt_config['tcp']['port']
    redis_host = mgmt_config['redis']['address']
    redis_port = mgmt_config['redis']['port']
    request_channel = mgmt_config['redis']['request_channel']
    response_channel = mgmt_config['redis']['response_channel']
    controller = HBProxyController(bind_address,
                                   protocols,
                                   upstream_host,
                                   upstream_port,
                                   True,
                                   redis_host,
                                   redis_port,
                                   request_channel,
                                   response_channel,
                                   True,
                                   tcp_mgmt_address,
                                   tcp_mgmt_port,
                                   plugins)

    return OperationFactory(controller)


def get_config(config_path):
    with open(config_path, 'r+') as config_file:
        config = yaml.load(config_file.read())

    return config


class ProxyInterfaceTCPTestCase(unittest.TestCase):

    def setUp(self):
        self.op_factory = get_op_factory()
        protoFactory = HBProxyMgmtProtocolFactory(self.op_factory)
        self.proto = protoFactory.buildProtocol(('127.0.0.1', 0))
        self.proto_transport = proto_helpers.StringTransport()
        self.proto.makeConnection(self.proto_transport)

    def _test(self, operation, expected):
        self.proto.dataReceived("'" + str(operation) + "'")
        self.assertEqual(self.proto_transport.value(), expected)

    def test_stop(self):
        operation = {"operation": "stop", "param": "n/a", "key": "abc"}
        expected = {"operation": "stop", "param": "n/a", "key": "abc"}

        return self._test(operation, expected)

    def test_start(self):
        operation = {"operation": "start", "param": "n/a", "key": "abc"}
        expected = {"operation": "stop", "param": "n/a", "key": "abc"}

        return self._test(operation, expected)

    def test_reset(self):
        operation = {"operation": "reset", "param": "n/a", "key": "abc"}
        expected = {"operation": "reset", "param": "n/a", "key": "abc"}

        return self._test(operation, expected)

    def test_reload(self):
        operation = {"operation": "reload", "param": "n/a", "key": "abc"}
        expected = {"operation": "reload", "param": "n/a", "key": "abc"}

        return self._test(operation, expected)

    def test_change_upstream_host(self):
        operation = {"operation": "upstream_host", "param": "192.168.1.1",
                     "key": "abc"}
        expected = {"operation": "upstream_host", "param": "192.168.1.1",
                    "key": "abc"}

        return self._test(operation, expected)

    def test_change_upstream_port(self):
        operation = {"operation": "upstream_port", "param": "8890",
                     "key": "abc"}
        expected = {"operation": "upstream_port", "param": "8890",
                    "key": "abc"}

        return self._test(operation, expected)

    def test_change_bind_address(self):
        operation = {"operation": "bind_address", "param": "192.168.1.1",
                     "key": "abc"}
        expected = {"operation": "bind_address", "param": "192.168.1.1",
                    "key": "abc"}

        return self._test(operation, expected)

    def test_change_bind_port(self):
        operation = {"operation": "bind_port", "param": "8890", "key": "abc"}
        expected = {"operation": "bind_port", "param": "8890", "key": "abc"}

        return self._test(operation, expected)

    def test_start_recording(self):
        operation = {"operation": "start_recording", "param": "1",
                     "key": "abc"}
        expected = {"operation": "start_recording", "param": "1",
                    "key": "abc"}

        return self._test(operation, expected)

    def test_stop_recording(self):
        operation = {"operation": "stop_recording", "param": "1", "key": "abc"}
        expected = {"operation": "stop_recording", "param": "1", "key": "abc"}

        return self._test(operation, expected)


class ProxyInterfaceRedisTestCase(ProxyInterfaceTCPTestCase):

    def setUp(self):
        self.op_factory = get_op_factory()
        protoFactory = HBProxyMgmtRedisSubscriberFactory(self.op_factory)
        self.proto = protoFactory.buildProtocol(('127.0.0.1', 6379))
        self.proto_transport = proto_helpers.StringTransport()
        self.proto.makeConnection(self.proto_transport)


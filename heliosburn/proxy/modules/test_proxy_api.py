from twisted.python import log
import json
from controller import OperationResponseFactory
from module import AbstractControllerTestModule


class TestControllerAPISuccess(AbstractControllerTestModule):

    def __init__(self):
        AbstractControllerTestModule.__init__(self)
        self.response_key = 'test'
        message = "execution successful"
        response_factory = OperationResponseFactory()
        self.op_response = response_factory.get_response(200,
                                                         message,
                                                         self.response_key)

    def get_expected(self):
        expected = json.dumps(self.op_response.response)
        return json.loads(expected)


class TestStopProxyAPI(TestControllerAPISuccess):
    """
    Used to teset the proxy controller API call 'stop'.
    """

    def get_message(self):
        response_message = "stop " + self.op_response.get_message()
        self.op_response.set_message(response_message)

        message = self._get_operation_message('stop',
                                              "n/a",
                                              self.response_key)
        return json.dumps(message)


test_stop_proxy = TestStopProxyAPI()


class TestStartProxyAPI(TestControllerAPISuccess):
    """
    Used to teset the proxy controller API call 'start'.
    """

    def get_message(self):
        response_message = "start " + self.op_response.get_message()
        self.op_response.set_message(response_message)

        message = self._get_operation_message('start',
                                              "n/a",
                                              self.response_key)
        return json.dumps(message)


test_start_proxy = TestStartProxyAPI()


class TestChangeUpstreamPortAPI(TestControllerAPISuccess):
    """
    Used to teset the proxy controller API call
    'upstream_port'.
    """

    def get_message(self):
        response_message = {'Change_upstream_port':
                            [self.op_response.get_message()],
                            }
        self.op_response.set_message(response_message)

        message = self._get_operation_message('upstream_port',
                                              "8989",
                                              self.response_key)
        return json.dumps(message)


test_upstream_port_proxy = TestChangeUpstreamPortAPI()


class TestChangeUpstreamHostAPI(TestControllerAPISuccess):
    """
    Used to teset the proxy controller API call
    'upstream_host'.
    """

    def get_message(self):
        response_message = {'Change_upstream_host':
                            [self.op_response.get_message()],
                            }
        self.op_response.set_message(response_message)

        message = self._get_operation_message('upstream_host',
                                              "127.0.0.1",
                                              self.response_key)
        return json.dumps(message)


test_upstream_host_proxy = TestChangeUpstreamHostAPI()


class TestChangeBindAddressAPI(TestControllerAPISuccess):
    """
    Used to teset the proxy controller API call
    'bind_address'.
    """

    def get_message(self):
        response_message = {'Change_bind_address':
                            [self.op_response.get_message()],
                            }
        self.op_response.set_message(response_message)

        message = self._get_operation_message('bind_address',
                                              "127.0.0.1",
                                              self.response_key)
        return json.dumps(message)


test_bind_address_proxy = TestChangeBindAddressAPI()


class TestReloadPluginsAPI(TestControllerAPISuccess):
    """
    Used to teset the proxy controller API call
    'reload'.
    """

    def get_message(self):
        response_message = {'Reload_plugins':
                            [self.op_response.get_message()],
                            }
        self.op_response.set_message(response_message)

        message = self._get_operation_message('reload',
                                              "n/a",
                                              self.response_key)
        return json.dumps(message)


test_reload_proxy = TestReloadPluginsAPI()


class TestResetPluginsAPI(TestControllerAPISuccess):
    """
    Used to teset the proxy controller API call
    'reset'.
    """

    def get_message(self):
        response_message = {'Reset_plugins':
                            [self.op_response.get_message()],
                            }
        self.op_response.set_message(response_message)

        message = self._get_operation_message('reset',
                                              "n/a",
                                              self.response_key)
        return json.dumps(message)


test_Reset_proxy = TestResetPluginsAPI()


class TestChangeBindPortAPI(TestControllerAPISuccess):
    """
    Used to teset the proxy controller API call
    'bind_port'.
    """

    def get_message(self):
        response_message = {'Change_bind_port':
                            [self.op_response.get_message()],
                            }
        self.op_response.set_message(response_message)

        message = self._get_operation_message('bind_port',
                                              8989,
                                              self.response_key)
        return json.dumps(message)


test_bind_port_proxy = TestChangeBindPortAPI()


class TestStartRecordingAPI(TestControllerAPISuccess):
    """
    Used to teset the proxy controller API call 'start_recording'.
    """

    def get_message(self):
        response_message = {'Started Recording':
                            [self.op_response.get_message()],
                            }
        self.op_response.set_message(response_message)

        recording_id = {'recording_id': 1}
        message = self._get_operation_message('start_recording',
                                              recording_id,
                                              self.response_key)
        return json.dumps(message)


test_start_recording = TestStartRecordingAPI()


class TestStopRecordingAPI(TestControllerAPISuccess):
    """
    Used to teset the proxy controller API call 'stop_recording'.
    """

    def get_message(self):
        response_message = "Stopped Recording: { "
        response_message += self.op_response.get_message() + ", "
        response_message += "}"

        self.op_response.set_message(response_message)
        recording_id = {'recording_id': 1}
        message = self._get_operation_message('stop_recording',
                                              recording_id,
                                              self.response_key)
        return json.dumps(message)


test_stop_recording = TestStopRecordingAPI()


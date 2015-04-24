import json
from twisted.python import log
from service.api import OperationResponseFactory
from module import AbstractAPITestModule


class TestAPISuccess(AbstractAPITestModule):

    def __init__(self):
        AbstractAPITestModule.__init__(self)
        self.response_key = 'test'
        message = "execution successful"
        response_factory = OperationResponseFactory()
        self.op_response = response_factory.get_response(200,
                                                         message,
                                                         self.response_key)

    def get_expected(self):
        expected = json.dumps(self.op_response.response)
        return json.loads(expected)


class TestStopProxyAPI(TestAPISuccess):
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


class TestStartProxyAPI(TestAPISuccess):
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


class TestChangeUpstreamPortAPI(TestAPISuccess):
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


class TestChangeUpstreamHostAPI(TestAPISuccess):
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


class TestChangeBindAddressAPI(TestAPISuccess):
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


class TestReloadPluginsAPI(TestAPISuccess):
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


class TestResetPluginsAPI(TestAPISuccess):
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


class TestChangeBindPortAPI(TestAPISuccess):
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


class TestStartRecordingAPI(TestAPISuccess):
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


class TestStopRecordingAPI(TestAPISuccess):
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


class TestBusyRecordingAPI(TestAPISuccess):
    """
    Used to teset the proxy controller API call 'start_recording',
    for a busy response.
    """

    def get_message(self):
        response_message = {'Busy':
                            [self.op_response.get_message()],
                            }
        self.op_response.set_message(response_message)

        recording_id = {'recording_id': 1}
        message = self._get_operation_message('start_recording',
                                              recording_id,
                                              self.response_key)
        return json.dumps(message)

    def evaluate(self, result):
        response = json.loads(result)
        expected = self.get_expected()
        result = self.assertEqual(501, response['code'])
        success_message = self.__class__.__name__ + ": "
        success_message += "SUCCESS!\n"
        success_message += "Result: " + str(result)
        print(success_message)

    def _publish_message(self, result):
        recording_id = {'recording_id': 1}
        start_m = self._get_operation_message('start_recording',
                                              recording_id,
                                              'abc123')
        self.redis_client.publish(self.redis_pub_queue, json.dumps(start_m))
        message = self.get_message()
        if message:
            self.redis_client.publish(self.redis_pub_queue, message)
        return result

test_busy_recording = TestBusyRecordingAPI()


class TestStatusAPI(TestAPISuccess):
    """
    Used to teset the proxy controller API call 'status'.
    """

    def get_message(self):
        response_message = {"status":
                            {
                                "module": "TrafficRecorder",
                                "state": "stopped",
                                "status": " "
                            }}

        self.op_response.set_message(response_message)
        message = self._get_operation_message('status',
                                              "TrafficRecorder",
                                              self.response_key)
        return json.dumps(message)

    def evaluate(self, result):
        response = json.loads(result)
        expected = self.get_expected()
        result = self.assertEqual(expected['message']['status']['state'],
                                  response['message']['status']['state'])
        success_message = self.__class__.__name__ + ": "
        success_message += "SUCCESS!\n"
        success_message += "Result: " + str(result)
        print(success_message)

test_status_proxy = TestStatusAPI()

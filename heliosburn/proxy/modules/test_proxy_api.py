from twisted.python import log
import json
from controller import OperationResponseFactory
from module import AbstractControllerTestModule


class TestControllerAPISuccess(AbstractControllerTestModule):

    def __init__(self):
        AbstractControllerTestModule.__init__(self)
        self.response_key = 'test'
        response_factory = OperationResponseFactory()
        self.op_response = response_factory.get_response(200,
                                                         "execution successful",
                                                         self.response_key)

    def get_expected(self):
        expected = json.dumps(self.op_response.response)
        return json.loads(expected)


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


from module import AbstractModule


class FaultInjection(AbstractModule):

    def handle_response(self, response, **kwargs):
        return response

    def handle_request(self, request, **kwargs):
        return request

    def reset(self):
        pass

fault_injection = FaultInjection()

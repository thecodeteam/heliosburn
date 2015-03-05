from module import AbstractModule
from twisted.python import log


class FaultInjection(AbstractModule):

    def handle_request(self, request, **kwargs):
        log.msg("FaultInjection started handling of request: %s" % request)
        return request

    def handle_response(self, response, **kwargs):
        return response

    def reset(self):
        pass

fault_injection = FaultInjection()

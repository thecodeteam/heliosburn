from module import AbstractModule
from twisted.python import log


#        log.msg("FaultInjection started handling of request: %s" % request)
class FaultInjection(AbstractModule):

    def handle_request(self, request):
        return request

    def handle_response(self, response):
        return response

    def reset(self):
        pass

fault_injection = FaultInjection()

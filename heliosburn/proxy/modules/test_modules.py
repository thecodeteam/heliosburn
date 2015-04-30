from module import AbstractModule
from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.python import log


class TestModifyStatus(AbstractModule):
    """
    This module changes the status code of the response
    """

    def start(self, result):
        agent = Agent(reactor)
        d = agent.request(
            'GET',
            'http://127.0.0.1:8880/',
            Headers({'User-Agent': ['TestModifyStatus']}),
            None)

        d.addCallback(self._response)
        return d

    def _response(self, response):
        print(response.headers.getRawHeaders('original_code'))
        print(response.code)

    def handle_response(self, response):
        """
        Alter the statuscode to be 400
        """
#        response.setHeader('original_code', response.code)
#        response.setResponseCode(400)
        return response

test_modify_status = TestModifyStatus()

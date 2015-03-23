from module import AbstractModule


class UnitTestModule(AbstractModule):
    """
    This module injects specific header/body attributes that proxy_core
    unittests looks for.
    """

    def handle_request(self, request, **kwargs):
        """
        Inject an easy-to-search-for header and body string into the request
        """
        self.setHeader('unit-test-request', 'unit testing request')
        self.setContent('unit testing body request')
        return request

    def handle_response(self, response,  **kwargs):
        """
        Inject an easy-to-search-for header and body string into the response
        """
        self.setHeader('unit-test-response', 'unit testing response')
        content = self.getContent()
        content += "\nunit testing body response"
        self.setContent(content)
        return response

unit_test_module = UnitTestModule()

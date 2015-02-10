from base import ProxyModuleBase


class UnitTestModule(ProxyModuleBase):
    def onRequest(self, **kwargs):
        self.setHeader('unit-test-request', 'unit testing request')
        self.setContent('unit testing body request')

    def onResponse(self, **kwargs):
        self.setHeader('unit-test-response', 'unit testing response')
        content = self.getContent()
        content += "\nunit testing body response"
        self.setContent(content)
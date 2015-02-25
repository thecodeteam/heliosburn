from proxy.modules import IModule
from proxy.modules import AbstractModule
from zope.interface import implements
from twisted.plugin import IPlugin


class UnitTestModule(AbstractModule):
    implements(IPlugin, IModule)
    """
    This module injects specific header/body attributes that proxy_core
    unittests looks for.
    """

    def get_name(self):
        self.name = "UnitTestModule"
        return self.name

    def onRequest(self, **kwargs):
        """
        Inject an easy-to-search-for header and body string into the request
        """
        self.setHeader('unit-test-request', 'unit testing request')
        self.setContent('unit testing body request')

    def onResponse(self, **kwargs):
        """
        Inject an easy-to-search-for header and body string into the response
        """
        self.setHeader('unit-test-response', 'unit testing response')
        content = self.getContent()
        content += "\nunit testing body response"
        self.setContent(content)

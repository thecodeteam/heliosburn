from proxy.modules import IModule
from proxy.modules import AbstractModule
from zope.interface import implements
from twisted.plugin import IPlugin


class allFail(AbstractModule):
    implements(IPlugin, IModule)

    def get_name(self):
        self.name = "allFail"
        return self.name

    def onResponse(self, **kwargs):
        self.response_object.handleStatus(version='HTTP/1.1',
                                          code=404,
                                          message="Sorry bub, Not found")

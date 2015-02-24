from proxy.iproxymodule import IModule
from zope.interface import implements
from twisted.plugin import IPlugin


class allFail(object):
    implements(IPlugin, IModule)

    def onResponse(self, **kwargs):
        self.response_object.handleStatus(version='HTTP/1.1',
                                          code=404,
                                          message="Sorry bub, Not found")

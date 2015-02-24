from proxy.iproxymodule import IModule
from zope.interface import implements
from twisted.plugin import IPlugin


class SampleModule(object):
    implements(IPlugin, IModule)

    def onRequest(self, **kwargs):

        headers = self.getAllHeaders()
        print headers
        self.setHeader('user-agent', 'Proxied by Helios')
        print self.getHeader('user-agent')
        self.setHeader('My-Super-Header', 'Mini moni mu')
        if self.hasHeader('Nice-Header'):
            self.removeHeader('Nice-Header')

        protocol = self.getProtocol()
        print protocol
        self.setProtocol('HTTP/1.1')

        method = self.getMethod()
        print method
        self.setMethod('PUT')

        uri = self.getURI()
        print uri
        # self.setURI('/modified/url')

        content = self.getContent()
        print content
        self.setContent('Content modified by HeliosBurn in REQUEST!')

    def onResponse(self, **kwargs):
        headers = self.getAllHeaders()
        print headers
        self.setHeader('Server', 'Proxied by Helios (Response)')
        print self.getHeader('Server')
        self.setHeader('My-Super-Header', 'Mini moni mu')
        if self.hasHeader('Nice-Header'):
            self.removeHeader('Nice-Header')

        protocol = self.getProtocol()
        print protocol
        self.setProtocol('HTTP/1.1')

        status_code = self.getStatusCode()
        print status_code
        # self.setStatusCode(500)

        status_desc = self.getStatusDescription()
        print status_desc
        # self.setStatusDescription("Internal Server Error")

        content = self.getContent()
        print content
        self.setContent('Content modified by HeliosBurn in RESPONSE!\n')

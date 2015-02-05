from base import ProxyModuleBase


class SampleModule(ProxyModuleBase):
    def onRequest(self, **kwargs):
        print self.request_object.clientproto
        self.request_object.clientproto = 'HTTP/1.1'
        #self.request_object.uri = '/modified/url/'
        self.request_object.requestHeaders.removeHeader('user-agent')
        self.request_object.requestHeaders.setRawHeaders('user-agent', ['HeliosBurn proxy ADDED ON REQUEST'])
        self.request_object.requestHeaders.addRawHeader('My-Header', '312')
        self.request_object.method = 'GET'

    def onResponse(self, **kwargs):
        print self.response_object.father.code
        print self.response_object.father.code_message
        print self.response_object.father.responseHeaders
        print self.response_object.father.clientproto
        self.response_object.father.responseHeaders.addRawHeader("Custom-Header", "Proxied by Helios ADDED ON RESPONSE")
from modules.base import ProxyModuleBase

class serialize(ProxyModuleBase):

    def onRequest(self, **kwargs):
        import json
        request_info = {}
        request_info['HEADERS'] = {}
        for key, value in self.proxy_object.requestHeaders.getAllRawHeaders():
            request_info['HEADERS'][key] = value
        request_info['METHOD'] = self.proxy_object.method
        request_info['URI'] = self.proxy_object.uri
        request_json = json.dumps(request_info)
        print "serializing request META-DATA for MQ"
        print request_json

    def onResponse(self, **kwargs):
        import json
        response_info = {}
        response_info['HEADERS'] = {}
        for key, value in self.proxy_object.father.responseHeaders.getAllRawHeaders():
            response_info['HEADERS'][key] = value
        response_info['CODE'] = self.proxy_object.father.code
        response_info['MESSAGE'] = self.proxy_object.father.code_message
        response_json = json.dumps(response_info)
        print "serializing response META-DATA for MQ"
        print response_json

from modules.base import ProxyModuleBase

class redisDump(ProxyModuleBase):

    def onRequest(self, **kwargs):
        import json
        request_info = {}
        request_info['HEADERS'] = {}
        for key, value in self.request_object.requestHeaders.getAllRawHeaders():
            request_info['HEADERS'][key] = value
        request_info['METHOD'] = self.request_object.method
        request_info['URI'] = self.request_object.uri
        request_json = json.dumps(request_info)
        print "serializing request META-DATA for MQ"
        print request_json

    def onResponse(self, **kwargs):
        import json
        import redis
        import datetime
        import time 
        import random 
        now = datetime.datetime.now()

        request = {}
        request['createdAt'] = now.strftime('%Y-%m-%d %H:%M:%S')
        request['httpProtocol'] = "HTTP/1.1" 
        request['method'] = self.request_object.method
        request['url'] = self.request_object.uri
        request['response'] = {}
        request['response']['createdAt'] = now.strftime('%Y-%m-%d %H:%M:%S')
        request['response']['httpProtocol'] = "HTTP/1.1"
        request['response']['statusCode'] = self.response_object.father.code
        request['response']['statusDescription'] = self.response_object.father.code_message
        request['response']['headers'] = {}
        for key, value in self.response_object.father.responseHeaders.getAllRawHeaders():
            request['response']['headers'][key] = value
        response_json = json.dumps(request)

        r = redis.StrictRedis(host = kwargs['redis_host'],
                                port = kwargs['redis_port'],
                                db = kwargs['redis_db'] )

        current_milli_time = lambda: int(round(time.time() * 1000))

        score = current_milli_time()

        # Remove traffic older than 10 seconds
        result = r.zremrangebyscore('test_traffic', '-inf', score - 10*1000)
        print '* Cleaned %d messages' % (result,)

        # Add request to set
        result = r.zadd('test_traffic', score, request)
        print '* Message with score %d sent successfully' % (score, ) if result else 'Could not sent message (%d)' % (score,)




class serialize(ProxyModuleBase):

    def onRequest(self, **kwargs):
        import json
        request_info = {}
        request_info['HEADERS'] = {}
        for key, value in self.request_object.requestHeaders.getAllRawHeaders():
            request_info['HEADERS'][key] = value
        request_info['METHOD'] = self.request_object.method
        request_info['URI'] = self.request_object.uri
        request_json = json.dumps(request_info)
        print "serializing request META-DATA for MQ"
        print request_json

    def onResponse(self, **kwargs):
        import json
        response_info = {}
        response_info['HEADERS'] = {}
        for key, value in self.response_object.father.responseHeaders.getAllRawHeaders():
            response_info['HEADERS'][key] = value
        response_info['CODE'] = self.response_object.father.code
        response_info['MESSAGE'] = self.response_object.father.code_message
        response_json = json.dumps(response_info)
        print "serializing response META-DATA for MQ"
        print response_json


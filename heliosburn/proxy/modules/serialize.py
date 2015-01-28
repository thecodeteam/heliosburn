import time
from modules.base import ProxyModuleBase

current_milli_time = lambda: int(round(time.time() * 1000))

class redisDump(ProxyModuleBase):
    """
    Extension of ProxyModuleBase interface used to serialize items to Redis.
    """



    def onRequest(self, **kwargs):
        pass

    def onResponse(self, **kwargs):
        """
        Default redis serializer. 

        Processes both proxy request and client response objects after
        response is received
        """
        import json
        import redis
        import datetime
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

        score = current_milli_time()

        # Remove traffic older than 10 seconds
        result = r.zremrangebyscore('heliosburn.traffic', '-inf', score - 10*1000)
        log.msg('* Cleaned %d messages' % (result,))

        # Add request to set
        result = r.zadd('heliosburn.traffic', score, response_json)
        if result:
            log.msg('* Message with score %d sent successfully' % (score, ) )
        else:
            log.msg('Could not send message (%d)' % (score,))




class serialize(ProxyModuleBase):
    """
    Extension of ProxyModuleBase interface used to serialize response and request objects to json
    """

    def onRequest(self, **kwargs):
        import json
        request_info = {}
        request_info['HEADERS'] = {}
        for key, value in self.request_object.requestHeaders.getAllRawHeaders():
            request_info['HEADERS'][key] = value
        request_info['METHOD'] = self.request_object.method
        request_info['URI'] = self.request_object.uri
        request_json = json.dumps(request_info)
        log.msg("serializing request META-DATA for MQ")
        log.msg(request_json)

    def onResponse(self, **kwargs):
        import json
        response_info = {}
        response_info['HEADERS'] = {}
        for key, value in self.response_object.father.responseHeaders.getAllRawHeaders():
            response_info['HEADERS'][key] = value
        response_info['CODE'] = self.response_object.father.code
        response_info['MESSAGE'] = self.response_object.father.code_message
        response_json = json.dumps(response_info)
        log.msg("serializing response META-DATA for MQ")
        log.msg(response_json)

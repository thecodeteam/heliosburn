import time

from base import ProxyModuleBase

current_milli_time = lambda: int(time.time() * 1000000)


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

        now = datetime.datetime.now()

        request = {}
        request['createdAt'] = now.strftime('%Y-%m-%d %H:%M:%S')  # TODO: get the real request date
        request['httpProtocol'] = "HTTP/1.1"
        request['method'] = self.request_object.method
        request['url'] = self.request_object.uri
        request['headers'] = {}
        for key, value in self.request_object.requestHeaders.getAllRawHeaders():
            request['headers'][key] = value
        request['response'] = {}
        request['response']['createdAt'] = now.strftime('%Y-%m-%d %H:%M:%S')  # TODO: get the real response date
        request['response']['httpProtocol'] = "HTTP/1.1"
        request['response']['statusCode'] = self.response_object.father.code
        request['response']['statusDescription'] = self.response_object.father.code_message
        request['response']['headers'] = {}
        for key, value in self.response_object.father.responseHeaders.getAllRawHeaders():
            request['response']['headers'][key] = value
        response_json = json.dumps(request)

        r = redis.StrictRedis(host=kwargs['redis_host'],
                              port=kwargs['redis_port'],
                              db=kwargs['redis_db'])

        score = current_milli_time()

        # Remove traffic older than 10 seconds
        result = r.zremrangebyscore('heliosburn.traffic', '-inf', score - 10 * 1000000)
        self.log.msg('* Cleaned %d messages' % (result,))

        # Add request to set
        result = r.zadd('heliosburn.traffic', score, response_json)
        if result:
            self.log.msg('* Message with score %d sent successfully' % (score, ))
        else:
            self.log.msg('Could not send message (%d)' % (score,))


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
        self.log.msg("serializing request META-DATA for MQ")
        self.log.msg(request_json)

    def onResponse(self, **kwargs):
        import json

        response_info = {}
        response_info['HEADERS'] = {}
        for key, value in self.response_object.father.responseHeaders.getAllRawHeaders():
            response_info['HEADERS'][key] = value
        response_info['CODE'] = self.response_object.father.code
        response_info['MESSAGE'] = self.response_object.father.code_message
        response_json = json.dumps(response_info)
        self.log.msg("serializing response META-DATA for MQ")
        self.log.msg(response_json)

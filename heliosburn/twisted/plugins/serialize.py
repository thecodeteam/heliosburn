from proxy.iproxymodule import IModule
from zope.interface import implements
from twisted.plugin import IPlugin
import time


current_milli_time = lambda: int(time.time() * 1000000)


class redisDump(object):
    implements(IPlugin, IModule)
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
        # TODO: get the real request date
        request['createdAt'] = now.strftime('%Y-%m-%d %H:%M:%S')
        request['httpProtocol'] = "HTTP/1.1"
        request['method'] = self.getMethod()
        request['url'] = self.getURI()
        request['headers'] = {}
        for key, value in self.request_object.requestHeaders.getAllRawHeaders():
            request['headers'][key] = value
        request['response'] = {}
        # TODO: get the real response date
        request['response']['createdAt'] = now.strftime('%Y-%m-%d %H:%M:%S')
        request['response']['httpProtocol'] = "HTTP/1.1"
        request['response']['statusCode'] = self.getStatusCode()
        request['response']['statusDescription'] = self.getStatusDescription()
        request['response']['headers'] = {}
        for key, value in self.getAllHeaders():
            request['response']['headers'][key] = value
        response_json = json.dumps(request)

        r = redis.StrictRedis(host=kwargs['redis_host'],
                              port=kwargs['redis_port'],
                              db=kwargs['redis_db'])

        score = current_milli_time()

        # Remove traffic older than 1 second
        result = r.zremrangebyscore('heliosburn.traffic', '-inf',
                                    score - 1 * 1000000)
        self.log.msg('* Cleaned %d messages' % (result,))

        # Add request to set
        result = r.zadd('heliosburn.traffic', score, response_json)
        if result:
            self.log.msg('* Message with score %d sent successfully'
                         % (score,))
        else:
            self.log.msg('Could not send message (%d)' % (score,))

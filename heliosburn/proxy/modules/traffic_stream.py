from module import AbstractModule
import time
import json
import redis
import datetime


class TrafficStream(AbstractModule):
    """
    Extension of AbstractModule class used to serialize items to Redis.
    """

    def _get_current_time(self):
        return int(time.time() * 1000000)

    def handle_response(self, response):
        """
        Default redis serializer.

        Processes both proxy request and client response objects after
        response is received
        """

        now = datetime.datetime.now()

        request = {}
        # TODO: get the real request date
        request['createdAt'] = now.strftime('%Y-%m-%d %H:%M:%S')
        request['httpProtocol'] = "HTTP/1.1"
        request['method'] = self.getMethod()
        request['url'] = self.getURI()
        request['headers'] = {}
        headers = self.request_object.requestHeaders.getAllRawHeaders()
        for key, value in headers:
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

        r = redis.StrictRedis(host='127.0.0.1',
                              port=6379,
                              db=0)

        score = self._get_current_time()

        # Remove traffic older than 1 second
        result = r.zremrangebyscore('heliosburn.traffic', '-inf',
                                    score - 1 * 1000000)
#        self.log.msg('* Cleaned %d messages' % (result,))

        # Add request to set
        result = r.zadd('heliosburn.traffic', score, response_json)
#        if result:
#            self.log.msg('* Message with score %d sent successfully'
#                         % (score,))
#        else:
#            self.log.msg('Could not send message (%d)' % (score,))

        return response


traffic_stream = TrafficStream()

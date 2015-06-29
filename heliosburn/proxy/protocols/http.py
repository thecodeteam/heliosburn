import uuid
import datetime
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.web.proxy import ProxyClient
from twisted.web.proxy import ReverseProxyRequest
from twisted.web.proxy import ReverseProxyResource
from twisted.web.proxy import ProxyClientFactory
from twisted.internet import reactor
from twisted.python import log
from txredis.client import RedisSubscriber
from django.utils.http import urlquote
from twisted.internet import protocol


class DRConnectionClient(Protocol):
    def dataReceived(self, data):
        pass


class DRConnectionClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        return DRConnectionClient()


class HBProxyClient(ProxyClient):
    """
    ProxyClient extension used to customize handling of proxy responses.
    See Twisted's ProxyClient API documentation for details.

    """
    def __init__(self, command, rest, version, headers, data, request):
        """
        Override ProxyClient.__init__ to:
            1. Set client HBModuleRegistry
            2. Set an intercept buffer
            3. Set an intercept header
            4. Set transaction_id

        """

        ProxyClient.__init__(self, command, rest, version, headers, data,
                             request)
        self.module_registry = request.module_registry
        self.buffer = ""
        self.header = {}
        now = datetime.datetime.now()
        self.father.response_createdAt = now.strftime('%Y-%m-%d %H:%M:%S')

    def _forward_response(self, response):
        content = self.father.response_content
        if not response.drop_connection and not response.reset_connection:
            # fix this... odd that it must exist
            if not self._finished:
                ProxyClient.handleResponsePart(self, content)
                ProxyClient.handleResponseEnd(self)
            log.msg("Response forwarded: " + str(response))
        else:
            if response.drop_connection:
                ProxyClient.handleResponsePart(self, content)
                ProxyClient.handleResponseEnd(self)
                response.transport.loseConnection()
                log.msg("Connection dropped")
            else:
                response.transport.abortConnection()
                log.msg("Connection reset")

    def handleResponsePart(self, buffer):
        self.buffer += buffer
        log.msg("handled partial response")

    def handleResponseEnd(self):
        self.father.response_content = self.buffer
        self.father.responseHeaders.setRawHeaders("Content-Length",
                                                  [len(self.father.
                                                       response_content)])
        self.module_registry.handle_response(self.father,
                                             self._forward_response)

#        log.msg("handled end of response: " + str(self.buffer))
        log.msg("handled end of response")

    def handleHeader(self, key, val):
        self.header[key] = val

    def handleEndHeaders(self):
        for k, v in self.header.iteritems():
            if not isinstance(v, list):
                v = [v]
            self.father.responseHeaders.setRawHeaders(k, v)


class HBProxyClientFactory(ProxyClientFactory):
    """
    Constructs an HBProxyClient and returns it

    """

    def __init__(self, command, rest, version, headers, data, request):
        """
        Override ProxyClientFactory.__init__ to return HBProxyClient

        """
        ProxyClientFactory.__init__(self, command, rest, version, headers,
                                    data, request)

    def buildProtocol(self, addr):
        """
        Override ProxyClientFactory.buildProtocol to return HBProxyClient

        """

        return HBProxyClient(self.command, self.rest, self.version,
                             self.headers, self.data, self.father)


class HBReverseProxyRequest(ReverseProxyRequest):
    """
    ReverseProxyRequest extension used to customize handling of proxy requests.
    See Twisted's ReverseProxyRequest API documentation for details.

    """

    proxyClientFactoryClass = HBProxyClientFactory

    def __init__(self, channel, queued, reactor=reactor):

        ReverseProxyRequest.__init__(self, channel, queued, reactor)
        now = datetime.datetime.now()
        self.createdAt = now.strftime('%Y-%m-%d %H:%M:%S')
        self.transaction_id = uuid.uuid1()
        self.request_id = uuid.uuid1()
        self.response_id = uuid.uuid1()

        self.module_registry = channel.site.resource.module_registry
        self.upstream_host = channel.site.resource.host
        self.upstream_port = channel.site.resource.port

        self.drop_connection = False
        self.reset_connection = False
        self.delay = 0

    def __repr__(self):
        request_headers = [[k, v] for (k, v)
                           in self.requestHeaders.getAllRawHeaders()]
        response_headers = [[k, v] for (k, v)
                            in self.responseHeaders.getAllRawHeaders()]
        request = {}
        request['createdAt'] = self.createdAt
        request['httpProtocol'] = self.clientproto
        request['method'] = self.method
        request['url'] = self.uri
        request['headers'] = {}
        request['headers']['request'] = request_headers
        request['headers']['response'] = response_headers
        return str(request)

    def _forward_request(self, request):
        if request:
            if not request.drop_connection and not request.reset_connection:
                clientFactory = self.proxyClientFactoryClass(
                    self.method, self.uri,
                    self.clientproto,
                    self.getAllHeaders(),
                    self.content.read(),
                    request
                )

                self.reactor.connectTCP(self.upstream_host, self.upstream_port,
                                        clientFactory)
                log.msg("Forwarding request to: " +
                        str(self.upstream_host) + ":" +
                        str(self.upstream_port))
            else:
                if request.drop_connection:
                    request.transport.loseConnection()
                    log.msg("Connection to: " +
                            str(self.upstream_host) + ":" +
                            str(self.upstream_port) + " dropped")
                else:
                    request.transport.abortConnection()
                    log.msg("Connection to: " +
                            str(self.upstream_host) + ":" +
                            str(self.upstream_port) + " reset")

    def process(self):
        """
        Implementation of Twisted's ReverseProxyReqeust.process() which
        processes request objects. Please see ReverseProxyRequest API
        documentation.
        """

        self.requestHeaders.setRawHeaders("host", [self.upstream_host])
        self.module_registry.handle_request(self, self._forward_request)


class HBReverseProxyResource(ReverseProxyResource):
    """
    ReverseProxyResource extension used to customize handling of proxy
    requests.  See Twisted's ReverseProxyResource API documentation for
    details.


    """
    proxyClientFactoryClass = HBProxyClientFactory

    def __init__(self, host, port, path, module_registry, reactor=reactor):
        self.module_registry = module_registry
        ReverseProxyResource.__init__(self, host, port, path, reactor)

    def getChild(self, path, request):
        """
        return host, port, URI, and reactor instance


        """
        return HBReverseProxyResource(
            self.host, self.port,
            self.path + '/' + urlquote(path, safe=""),
            self.module_registry,
            self.reactor)


class HBProxyMgmtRedisSubscriber(RedisSubscriber):

    def __init__(self, request_channel, op_factory, *args, **kwargs):
        RedisSubscriber.__init__(self, *args, **kwargs)
        self.channel = request_channel
        self.op_factory = op_factory

    def subscribe(self):
        super(HBProxyMgmtRedisSubscriber, self).subscribe(self.channel)

    def set_redis_client(self, redis_client):
        self.redis_client = redis_client

    def messageReceived(self, channel, message):
        operation = self.op_factory.get_operation(message)
        return operation.execute()

    def channelSubscribed(self, channel, numSubscriptions):
        log.msg("HBproxy subscribed to channel: " +
                channel +
                " it is subscriber 1 of : " +
                str(numSubscriptions))

    def channelUnSubscribed(self, channel, numSubscriptions):
        log.msg("HBproxy unsubscribed from channel: " +
                channel +
                " there are : " +
                str(numSubscriptions) +
                " subscribers remaining ")


class HBProxyMgmtRedisSubscriberFactory(protocol.Factory):

    def __init__(self, request_channel, op_factory):
        self.request_channel = request_channel
        self.op_factory = op_factory

    def buildProtocol(self, addr):
        return HBProxyMgmtRedisSubscriber(self.request_channel,
                                          self.op_factory)

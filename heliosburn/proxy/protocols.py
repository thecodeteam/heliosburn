import yaml
from io import BytesIO
from twisted.web.proxy import ProxyClient
from twisted.web.proxy import ReverseProxyRequest
from twisted.web.proxy import ReverseProxyResource
from twisted.web.proxy import ProxyClientFactory
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.python import log
from txredis.client import RedisClient
from txredis.client import RedisClientFactory
from txredis.client import RedisSubscriber
from django.utils.http import urlquote
from twisted.internet import protocol
from module import Registry


class HBProxyClient(ProxyClient):
    """
    ProxyClient extension used to customize handling of proxy responses.
    See Twisted's ProxyClient API documentation for details.

    """
    def __init__(self, command, rest, version, headers, data, father,
                 module_registry):
        """
        Override ProxyClient.__init__ to accept HBModuleRegistry
        as a parameter

        """

        self.module_registry = module_registry
        ProxyClient.__init__(self, command, rest, version, headers, data,
                             father)

    def _forward_response(self, response):

        self.father.response_content = response
        self.father.headers['Content-Length'] = len(self.father.
                                                    content.getvalue())
        ProxyClient.handleResponsePart(self, self.father.content.getvalue())

    def handleResponsePart(self, buffer):
        print("hello world")
        self.module_registry.handle_response(BytesIO(buffer),
                                             self._forward_response)


class HBProxyClientFactory(ProxyClientFactory):
    """
    Constructs an HBProxyClient and returns it

    """

    def __init__(self, command, rest, version, headers, data, father,
                 module_registry):
        """
        Override ProxyClientFactory.__init__ to return HBProxyClient

        """
        self.module_registry = module_registry
        ProxyClientFactory.__init__(self, command, rest, version, headers,
                                    data, father)

    def buildProtocol(self, addr):
        """
        Override ProxyClientFactory.buildProtocol to return HBProxyClient

        """

        return HBProxyClient(self.command, self.rest, self.version,
                             self.headers, self.data, self.father,
                             self.module_registry)


class HBReverseProxyRequest(ReverseProxyRequest):
    """
    ReverseProxyRequest extension used to customize handling of proxy requests.
    See Twisted's ReverseProxyRequest API documentation for details.

    """

    proxyClientFactoryClass = HBProxyClientFactory

    def __init__(self, channel, queued, reactor=reactor):

        ReverseProxyRequest.__init__(self, channel, queued, reactor)
        # need to refactor this
        plugins = self.get_config("./modules.yaml")
        config = self.get_config("./config.yaml")
        proxy_config = config['proxy']

        self.module_registry = Registry(plugins)
        self.upstream_host = proxy_config['upstream']['address']
        self.upstream_port = proxy_config['upstream']['port']

    def get_config(self, config_path):
        with open(config_path, 'r+') as config_file:
            config = yaml.load(config_file.read())

        return config

    def _forward_request(self, request):
        log.msg("forwarding pipeline processed request: %s" % request)

        clientFactory = self.proxyClientFactoryClass(self.method, self.uri,
                                                     self.clientproto,
                                                     self.getAllHeaders(),
                                                     self.content.read(),
                                                     request,
                                                     self.module_registry)

        self.reactor.connectTCP(self.upstream_host, self.upstream_port,
                                clientFactory)

    def process(self):
        """
        Implementation of Twisted's ReverseProxyReqeust.process() which
        processes request objects. Please see ReverseProxyRequest API
        documentation.
        """

        self.requestHeaders.setRawHeaders(b"host", [self.upstream_host])
        log.msg("Started processing of request: %s" % self)
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
        operation.execute()

    def channelSubscribed(self, channel, numSubscriptions):
        log.msg("HBproxy subscribed to channel: "
                + channel
                + " it is subscriber 1 of : "
                + str(numSubscriptions))

    def channelUnSubscribed(self, channel, numSubscriptions):
        log.msg("HBproxy unsubscribed from channel: "
                + channel
                + " there are : "
                + str(numSubscriptions)
                + " subscribers remaining ")


class HBProxyMgmtRedisSubscriberFactory(protocol.Factory):

    def __init__(self, request_channel, op_factory):
        self.request_channel = request_channel
        self.opt_factory = op_factory

    def buildProtocol(self, addr):
        return HBProxyMgmtRedisSubscriber(self.request_channel,
                                          self.opt_factory)


class HBProxyMgmtProtocol(protocol.Protocol):

    def __init__(self, op_factory):
        self.op_factory = op_factory

    def dataReceived(self, data):
        self.op_factory.get_operation(data)


class HBProxyMgmtProtocolFactory(protocol.Factory):

    def __init__(self, op_factory):
        self.op_factory = op_factory

    def buildProtocol(self, addr):
        return HBProxyMgmtProtocol(self.op_factory)


#!/usr/bin/env python

# proxy_core provides ReverseProxy functionality to HeliosBurn
# If invoked with the single command line parameter 'unittests',
# it discards all modules from config.yaml, and loads
# only the 'unittest_module.py' module, necessary for unit tests.
# To run unit tests against proxy_core.py, execute `python -m unittest tests`

from os.path import dirname, abspath
from inspect import getsourcefile

from django.utils.http import urlquote
import yaml
import sys
import argparse
import json
from io import BytesIO
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet import defer
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.web import proxy
from twisted.web import server
from twisted.python import log
from twisted.web.proxy import ReverseProxyRequest
from twisted.web.proxy import ReverseProxyResource
from twisted.web.proxy import ProxyClientFactory
from twisted.web.proxy import ProxyClient
from txredis.client import RedisClient
from txredis.client import RedisClientFactory
from txredis.client import RedisSubscriber
from plugins import Registry


class HBProxyClient(ProxyClient):
    """
    ProxyClient extension used to customize handling of proxy responses.
    See Twisted's ProxyClient API documentation for details.

    """
    def __init__(self, command, rest, version, headers, data, father,
                 plugin_registry):
        """
        Override ProxyClient.__init__ to accept HBModuleRegistry
        as a parameter

        """

        self.plugin_registry = plugin_registry
        ProxyClient.__init__(self, command, rest, version, headers, data,
                             father)

    def handleStatus(self, version, code, message):
        """
        Invoked after a status code and message are received
        """
        ProxyClient.handleStatus(self, version, code, message)
#        self.plugin_registry.run_plugins(context='response',
#                                         request_object=self.father)

    def handleResponsePart(self, buffer):

        self.father.response_content = BytesIO(buffer)
        self.plugin_registry.run_plugins(context='response',
                                         request_object=self.father)

        self.father.headers['Content-Length'] = len(self.father.
                                                    content.getvalue())
        ProxyClient.handleResponsePart(self, self.father.content.getvalue())

    def handleHeader(self, key, value):
        """
        Invoked once for every Header received in a response
        """
        ProxyClient.handleHeader(self, key, value)


class HBProxyClientFactory(ProxyClientFactory):
    """
    Constructs an HBProxyClient and returns it

    """

    def __init__(self, command, rest, version, headers, data, father,
                 plugin_registry):
        """
        Override ProxyClientFactory.__init__ to return HBProxyClient

        """

        self.plugin_registry = plugin_registry
        ProxyClientFactory.__init__(self, command, rest, version, headers,
                                    data, father)

    def buildProtocol(self, addr):
        """
        Override ProxyClientFactory.buildProtocol to return HBProxyClient

        """

        return HBProxyClient(self.command, self.rest, self.version,
                             self.headers, self.data, self.father,
                             self.plugin_registry)


class HBReverseProxyRequest(ReverseProxyRequest):
    """
    ReverseProxyRequest extension used to customize handling of proxy requests.
    See Twisted's ReverseProxyRequest API documentation for details.

    """

    proxyClientFactoryClass = HBProxyClientFactory

    def __init__(self, upstream_host, upstream_port, channel,
                 queued, plugin_registry, reactor=reactor):

        self.plugin_registry = plugin_registry
        self.upstream_host = upstream_host
        self.upstream_port = upstream_port

        ReverseProxyRequest.__init__(self, channel, queued, reactor)

    def process(self):
        """
        Implementation of Twisted's ReverseProxyReqeust.process() which
        processes request objects. Please see ReverseProxyRequest API
        documentation.
        """

        self.plugin_registry.run_plugins(context='request',
                                         request_object=self)
        log.msg("VERB: {}.method, URI: {}.uri, HEADERS: {}.requestHeaders".
                format(self, self, self))

        self.requestHeaders.setRawHeaders(b"host", [self.upstream_host])
        clientFactory = self.proxyClientFactoryClass(self.method, self.uri,
                                                     self.clientproto,
                                                     self.getAllHeaders(),
                                                     self.content.read(),
                                                     self,
                                                     self.plugin_registry)

        self.reactor.connectTCP(self.upstream_host, self.upstream_port,
                                clientFactory)


class HBReverseProxyResource(ReverseProxyResource):
    """
    ReverseProxyResource extension used to customize handling of proxy
    requests.  See Twisted's ReverseProxyResource API documentation for
    details.


    """
    proxyClientFactoryClass = HBProxyClientFactory

    def __init__(self, host, port, path, plugin_registry, reactor=reactor):
        self.plugin_registry = plugin_registry
        ReverseProxyResource.__init__(self, host, port, path, reactor)

    def getChild(self, path, request):
        """
        return host, port, URI, and reactor instance


        """
        return HBReverseProxyResource(
            self.host, self.port,
            self.path + '/' + urlquote(path, safe=""),
            self.plugin_registry,
            self.reactor)


class HBProxyMgmtRedisSubscriber(RedisSubscriber):

    def __init__(self, proxy, redis_endpoint, request, response,
                 *args, **kwargs):
        RedisSubscriber.__init__(self, *args, **kwargs)
        self.channel = request
        self.proxy = proxy
        self.op_factory = RedisOperationFactory(proxy, redis_endpoint,
                                                response)

    def subscribe(self):
        super(HBProxyMgmtRedisSubscriber, self).subscribe(self.channel)

    def set_redis_client(self, redis_client):
        self.redis_client = redis_client

    def messageReceived(self, channel, message):
        operation = self.op_factory.get_operation(message)
        operation.execute()
#       self.redis_client.publish(self.hb_proxy.response_channel, response)

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

    def __init__(self, proxy, redis_endpoint, request, response):
        self.proxy = proxy
        self.request = request
        self.response = response
        self.endpoint = redis_endpoint

    def buildProtocol(self, addr):
        return HBProxyMgmtRedisSubscriber(self.proxy, self.endpoint,
                                          self.request, self.response)


class HBProxyMgmtProtocol(protocol.Protocol):

    def __init__(self, hb_proxy):
        self.op_factory = TcpOperationFactory(hb_proxy)

    def dataReceived(self, data):
        self.op_factory.get_operation(data)


class HBProxyMgmtProtocolFactory(protocol.Factory):

    def __init__(self, hb_proxy):
        self.hb_proxy = hb_proxy

    def buildProtocol(self, addr):
        return HBProxyMgmtProtocol(self.hb_proxy)


class OperationResponse(object):

    def __init__(self, code, message, key):

        self.response = {'code': code,
                         'message': message,
                         'key': key
                         }

    def get_code(self):
        return self.response['code']

    def get_message(self):
        return self.response['message']

    def set_code(self, code):
        self.response['code'] = code

    def set_message(self, message):
        self.response['message'] = message

    def send(self):
        pass


class RedisOperationResponse(OperationResponse):

    def __init__(self, code, message, key, redis_endpoint, response_channel):

        OperationResponse.__init__(self, code, message, key)

        self.response_channel = response_channel

        redis_conn = redis_endpoint.connect(RedisClientFactory())
        redis_conn.addCallback(self.set_redis_client)

    def set_redis_client(self, redis_client):
        print("got redis client")
        self.redis_client = redis_client

    def send(self, result):
        self.redis_client.publish(self.response_channel, self.response)


class OperationResponseFactory(object):

    def get_response(self, code, message, key):
        pass


class RedisOperationResponseFactory(OperationResponseFactory):

    def __init__(self, redis_endpoint, response_channel):
        self.reactor = reactor
        self.response_channel = response_channel
        self.redis_endpoint = redis_endpoint

    def get_response(self, code, message, key):
        response = RedisOperationResponse(code, message, key,
                                          self.redis_endpoint,
                                          self.response_channel)
        return response


class TcpOperationResponseFactory(OperationResponseFactory):

    def get_response(self, code, message, key):
        pass


class ControllerOperation(object):

    def __init__(self, response, key):
        self.operation = defer.Deferred()
        self.response = response
        self.key = key

    def execute(self):
        return self.operation.callback(self.response)


class StopProxy(ControllerOperation):

    def __init__(self, proxy, response_factory, key):
        ControllerOperation.__init__(self, response_factory, key)
        self.proxy = proxy
        self.response = response_factory.get_response(200,
                                                      "execution successful",
                                                      self.key)
        self.operation.addCallback(self.stop)
        self.operation.addCallback(self.response.send)

    def stop(self, result):
        self.proxy.stopListening()
        self.response.set_message("stop " + self.response.get_message())


class OperationFactory(object):

    def __init__(self, proxy):
        self.proxy = proxy
        self.response_factory = OperationResponseFactory()

    def get_operation(self, message):
        op_string = json.loads(message)
        operation = None

        if "stop" == op_string['operation']:
            operation = StopProxy(self.proxy,
                                  self.response_factory,
                                  op_string['key'])

        if "start" == op_string['operation']:
            #           self.hb_proxy.start_proxy()
            operation = "proxy started"

        if "reload" == op_string['operation']:
            #           self.hb_proxy.reload_plugins()
            operation = "plugins reloaded"

        if "reset" == op_string['operation']:
            #           self.hb_proxy.reset_plugins()
            operation = "plugins reset"

        if "upstream_port" == op_string['operation']:
            #           self.hb_proxy.set_upstream_port(op_string['param'])
            operation = "upstream port changed"

        if "upstream_host" == op_string['operation']:
            #           self.hb_proxy.set_upstream_host(op_string['param'])
            operation = "upstream host changed"

        if "listen_address" == op_string['operation']:
            #           self.hb_proxy.set_listen_address(op_string['param'])
            operation = "listen address changed"

        if "listen_port" == op_string['operation']:
            #           self.hb_proxy.set_listen_port(op_string['command']['param'])
            operation = "listen port changed"

        return operation


class RedisOperationFactory(OperationFactory):

    def __init__(self, proxy, redis_endpoint, response_channel):
        OperationFactory.__init__(self, proxy)
        self.response_factory = RedisOperationResponseFactory(redis_endpoint,
                                                              response_channel)


class TcpOperationFactory(OperationFactory):

    def __init__(self, hb_proxy, response_channel):
        OperationFactory.__init__(hb_proxy)
        self.repsponse_factory = TcpOperationResponseFactory()


class HBProxyController(object):

    def __init__(self, bind_address, protocols, upstream_host, upstream_port,
                 redis_mgmt, redis_host, redis_port, request_channel,
                 response_channel, tcp_mgmt, tcp_mgmt_address, tcp_mgmt_port,
                 plugins):

        # Set a marker for our code path
        self.base_path = dirname(abspath(getsourcefile(lambda _: None)))
        self.bind_address = bind_address
        self.protocols = protocols
        self.upstream_host = upstream_host
        self.upstream_port = upstream_port
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.request_channel = request_channel
        self.response_channel = response_channel
        self.tcp_mgmt_address = tcp_mgmt_address
        self.tcp_mgmt_port = tcp_mgmt_port

        self.plugin_registry = Registry(plugins)
        self.site = server.Site(proxy.ReverseProxyResource(self.upstream_host,
                                self.upstream_port, ''))

        self.mgmt_protocol_factory = HBProxyMgmtProtocolFactory(self)

    def _start_logging(self):

        setStdout = True
        log.startLogging(sys.stdout)

    def stop_proxy(self):
        self.proxy.stopListening()

    def start_proxy(self):
        resource = HBReverseProxyResource(self.upstream_host,
                                          self.upstream_port, '',
                                          self.plugin_registry)
        f = server.Site(resource)
        f.requestFactory = HBReverseProxyRequest
        self.proxy = reactor.listenTCP(self.protocols['http'], f,
                                       interface=self.bind_address)

    def reset_plugins(self):
        self.plugin_registry = Registry(self.config)
        self.plugin_registry.run_plugins(context='None')

    def reload_plugins(self):
        self.plugin_registry = Registry(self.config)
        self.plugin_registry.run_plugins(context='None')

    def set_upstream_port(self, port):
        self.stop_proxy()
        self.upstream_port = port
        self.start_proxy()

    def set_upstream_host(self, host):
        self.stop_proxy()
        self.upstream_host = host
        self.start_proxy()

    def set_listen_port(self, port):
        self.listen_port = port
        self.stop_proxy()
        self.start_proxy()

    def set_listen_address(self, address):
        self.listen_address = address
        self.stop_proxy()
        self.start_proxy()

    def subscribe(self, redis):
        response = redis.subscribe()

    def run(self):
        self.plugin_registry.run_plugins(context='None')

        reactor.listenTCP(self.tcp_mgmt_port, self.mgmt_protocol_factory,
                          interface=self.tcp_mgmt_address)

        self.start_proxy()
        self._start_logging()
        redis_endpoint = TCP4ClientEndpoint(reactor, self.redis_host,
                                            self.redis_port)
        redis_conn = redis_endpoint.connect(
            HBProxyMgmtRedisSubscriberFactory(self.proxy, redis_endpoint,
                                              self.request_channel,
                                              self.response_channel))
        redis_conn.addCallback(self.subscribe)
        reactor.run()


def get_config(config_path):
    with open(config_path, 'r+') as config_file:
        config = yaml.load(config_file.read())

    return config


def get_arg_parser():

    description = " Helios Burn Proxy Server:  \n\n"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--config_path',
                        default="./config.yaml",
                        dest='config_path',
                        help='Path to output config file. Default: '
                        + ' ./config.yamle')

    parser.add_argument('--tcp_mgmt',
                        action="store_true",
                        dest='tcp_mgmt',
                        help='If set will listen for proxy mgmt commands on'
                        + ' a TCP port as well as subscribe to the request'
                        + ' channel. Default: false')

    parser.add_argument('--tcp_address',
                        dest='tcp_mgmt_address',
                        help='If the proxy mgmt interface is listening '
                        + ' on a tcp socket, this option will set the address'
                        + ' on which to listen.')

    parser.add_argument('--tcp_port',
                        dest='tcp_mgmt_port',
                        help='If the proxy mgmt interface is listening '
                        + ' on a tcp socket, this option will set the port'
                        + ' on which to listen.')

    parser.add_argument('--redis_mgmt',
                        action="store_true",
                        dest='redis_mgmt',
                        help='If set will subscribe to a given REDIS'
                        + ' channel for proxy mgmt commands'
                        + ' Default: true')

    parser.add_argument('--redis_address',
                        dest='redis_address',
                        help='If the proxy mgmt interface is listening '
                        + ' on a tcp socket, this option will set the address'
                        + ' on which to listen.')

    parser.add_argument('--redis_port',
                        dest='redis_port',
                        help='If the proxy mgmt interface is listening '
                        + ' on a tcp socket, this option will set the port'
                        + ' on which to listen.')

    parser.add_argument('--request_channel',
                        dest='request_channel',
                        help='If the proxy mgmt interface is set to use redis'
                        + ', this option will set the channel to which it '
                        + ' should subscribe.')

    parser.add_argument('--response_channel',
                        dest='response_channel',
                        help='If the proxy mgmt interface is set to use redis'
                        + ', this option will set the channel to which it '
                        + ' should publish.')

    return parser


def main():
    """
    Entry point for starting the proxy
    """
    args = get_arg_parser().parse_args()
    config_path = args.config_path

    config = get_config(config_path)
    proxy_config = config['proxy']
    mgmt_config = config['mgmt']

    bind_address = proxy_config['bind_address']
    protocols = proxy_config['protocols']
    upstream_host = proxy_config['upstream']['address']
    upstream_port = proxy_config['upstream']['port']
    tcp_mgmt_address = mgmt_config['tcp']['address']
    tcp_mgmt_port = mgmt_config['tcp']['port']
    redis_address = mgmt_config['redis']['address']
    redis_port = mgmt_config['redis']['port']
    request_channel = mgmt_config['redis']['request_channel']
    response_channel = mgmt_config['redis']['response_channel']

    print (redis_port)

    if args.tcp_mgmt:
        if args.tcp_mgmt_address:
            tcp_mgmt_address = args.tcp_mgmt_address

        if args.tcp_mgmt_port:
            tcp_mgmt_port = args.tcp_mgmt_port

    if args.redis_mgmt:
        if args.redis_address:
            redis_address = args.redis_address
        if args.redis_port:
            redis_port = args.redis_address
        if args.request_channel:
            request_channel = args.request_channel
        if args.response_channel:
            response_channel = args.response_channel

    plugins = get_config("./modules.yaml")

    proxy_controller = HBProxyController(bind_address, protocols,
                                         upstream_host, upstream_port,
                                         args.redis_mgmt, redis_address,
                                         redis_port, request_channel,
                                         response_channel, args.tcp_mgmt,
                                         tcp_mgmt_address, tcp_mgmt_port,
                                         plugins)
    proxy_controller.run()

if __name__ == "__main__":
    main()

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
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.web import proxy
from twisted.web import server
from twisted.python import log
from twisted.web.proxy import ReverseProxyRequest
from twisted.web.proxy import ReverseProxyResource
from twisted.web.proxy import ProxyClientFactory
from twisted.web.proxy import ProxyClient
from io import BytesIO
from txredis.client import RedisClient, RedisClientFactory, RedisSubscriber
from twisted.internet.endpoints import TCP4ClientEndpoint


class HBProxyModuleRegistry(object):

    def __init__(self, modules):
        self.modules = modules

    def _get_class(self, mod_dict):
        """
        Simple function which returns a class dynamically
        when passed a dictionary containing the appropriate
        information about a proxy module

        """
        log.msg("mod_dict: %s" % mod_dict)
        module_path = mod_dict['path']
        class_name = mod_dict['name']
        try:
            module = __import__(module_path, fromlist=[class_name])
        except ImportError:
            raise ValueError("Module '%s' could not be imported" %
                             (module_path,))

        try:
            class_ = getattr(module, class_name)
        except AttributeError:
            raise ValueError("Module '%s' has no class '%s'" % (module_path,
                                                                class_name,))
        return class_

    def run_modules(self, context, request_object=None):
        """
        Runs all proxy modules in the order specified in config.yaml

        """
#       for module_dict in self.modules:
#           class_ = self._get_class(module_dict)
#           instance_ = class_(context=context,
#                              request_object=request_object,
#                              run_contexts=module_dict['run_contexts'])
#           instance_.run(**module_dict['kwargs'])


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

    def handleStatus(self, version, code, message):
        """
        Invoked after a status code and message are received
        """
        ProxyClient.handleStatus(self, version, code, message)
#        self.module_registry.run_modules(context='response',
#                                         request_object=self.father)

    def handleResponsePart(self, buffer):

        self.father.response_content = BytesIO(buffer)
        self.module_registry.run_modules(context='response',
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

    def __init__(self, upstream_host, upstream_port, channel,
                 queued, module_registry, reactor=reactor):

        self.module_registry = module_registry
        self.upstream_host = upstream_host
        self.upstream_port = upstream_port

        ReverseProxyRequest.__init__(self, channel, queued, reactor)

    def process(self):
        """
        Implementation of Twisted's ReverseProxyReqeust.process() which
        processes request objects. Please see ReverseProxyRequest API
        documentation.
        """

        self.module_registry.run_modules(context='request',
                                         request_object=self)
        log.msg("VERB: {}.method, URI: {}.uri, HEADERS: {}.requestHeaders".
                format(self, self, self))

        self.requestHeaders.setRawHeaders(b"host", [self.upstream_host])
        clientFactory = self.proxyClientFactoryClass(self.method, self.uri,
                                                     self.clientproto,
                                                     self.getAllHeaders(),
                                                     self.content.read(),
                                                     self,
                                                     self.module_registry)

        self.reactor.connectTCP(self.upstream_host, self.upstream_port,
                                clientFactory)


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

    def __init__(self, hb_proxy, channel, *args, **kwargs):
        RedisSubscriber.__init__(self, *args, **kwargs)
        self.channel = channel
        self.hb_proxy = hb_proxy
        self.command_parser = HBProxyMgmtCommandParser(hb_proxy)
        redis_endpoint = TCP4ClientEndpoint(reactor, hb_proxy.redis_host,
                                            hb_proxy.redis_port)
        redis_conn = redis_endpoint.connect(RedisClientFactory())
        redis_conn.addCallback(self.set_redis_client)

    def subscribe(self):
        super(HBProxyMgmtRedisSubscriber, self).subscribe(self.channel)

    def set_redis_client(self, redis_client):
        self.redis_client = redis_client

    def messageReceived(self, channel, message):
        response = self.command_parser.parse(message)
        self.redis_client.publish(self.hb_proxy.response_channel, response)

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

    def __init__(self, hb_proxy, channel):
        self.hb_proxy = hb_proxy
        self.channel = channel

    def buildProtocol(self, addr):
        return HBProxyMgmtRedisSubscriber(self.hb_proxy, self.channel)


class HBProxyMgmtProtocol(protocol.Protocol):

    def __init__(self, hb_proxy):
        self.command_parser = HBProxyMgmtCommandParser(hb_proxy)

    def dataReceived(self, data):
        self.command_parser.parse(data)


class HBProxyMgmtProtocolFactory(protocol.Factory):

    def __init__(self, hb_proxy):
        self.hb_proxy = hb_proxy

    def buildProtocol(self, addr):
        return HBProxyMgmtProtocol(self.hb_proxy)


class HBProxyMgmtCommandParser(object):

    def __init__(self, hb_proxy):
        self.hb_proxy = hb_proxy

    def parse(self, message):
        command_string = json.loads(message)
        response_string = ""

        if "stop" == command_string['operation']:
            self.hb_proxy.stop_proxy()
            response_string = "proxy stopped"

        if "start" == command_string['operation']:
            self.hb_proxy.start_proxy()
            response_string = "proxy started"

        if "reload" == command_string['operation']:
            self.hb_proxy.reload_modules()
            response_string = "modules reloaded"

        if "reset" == command_string['operation']:
            self.hb_proxy.reset_modules()
            response_string = "modules reset"

        if "upstream_port" == command_string['operation']:
            self.hb_proxy.set_upstream_port(command_string['param'])
            response_string = "upstream port changed"

        if "upstream_host" == command_string['operation']:
            self.hb_proxy.set_upstream_host(command_string['param'])
            response_string = "upstream host changed"

        if "listen_address" == command_string['operation']:
            self.hb_proxy.set_listen_address(command_string['param'])
            response_string = "listen address changed"

        if "listen_port" == command_string['operation']:
            self.hb_proxy.set_listen_port(command_string['command']['param'])
            response_string = "listen port changed"

        return response_string


class HBProxy(object):

    def __init__(self, bind_address, protocols, upstream_host, upstream_port,
                 redis_mgmt, redis_host, redis_port, request_channel,
                 response_channel, tcp_mgmt, tcp_mgmt_address, tcp_mgmt_port,
                 modules):

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

        self.module_registry = HBProxyModuleRegistry(modules)
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
                                          self.module_registry)
        f = server.Site(resource)
        f.requestFactory = HBReverseProxyRequest
        self.proxy = reactor.listenTCP(self.protocols['http'], f,
                                       interface=self.bind_address)

    def reset_modules(self):
        self._load_config()
        self.module_registry = HBProxyModuleRegistry(self.config)
        self.module_registry.run_modules(context='None')

    def reload_modules(self):
        self._load_config()
        self.module_registry = HBProxyModuleRegistry(self.config)
        self.module_registry.run_modules(context='None')

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
        print(response)

    def run(self):
        self.module_registry.run_modules(context='None')

        reactor.listenTCP(self.tcp_mgmt_port, self.mgmt_protocol_factory,
                          interface=self.tcp_mgmt_address)

        self.start_proxy()
        self._start_logging()
        redis_endpoint = TCP4ClientEndpoint(reactor, self.redis_host,
                                            self.redis_port)
        redis_conn = redis_endpoint.connect(
            HBProxyMgmtRedisSubscriberFactory(self, self.request_channel))
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

    modules = get_config("./modules.yaml")

    hb_proxy = HBProxy(bind_address, protocols, upstream_host, upstream_port,
                       args.redis_mgmt, redis_address, redis_port,
                       request_channel, response_channel, args.tcp_mgmt,
                       tcp_mgmt_address, tcp_mgmt_port, modules)
    hb_proxy.run()

if __name__ == "__main__":
    main()

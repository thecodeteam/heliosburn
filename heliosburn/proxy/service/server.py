#!/usr/bin/env python

# proxy_core provides ReverseProxy functionality to HeliosBurn
# If invoked with the single command line parameter '--test',
# it discards all modules from config.yaml except those in the,
# test section.

import sys
import json
import logging
import logging.config
from settings import Common
from service.api import RedisOperationFactory
from twisted.internet import reactor
from twisted.internet import endpoints
from twisted.internet import defer
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.web import proxy
from twisted.web import server
from twisted.web import resource
from twisted.python import log
from module import Registry
from protocols.http import HBReverseProxyRequest
from protocols.http import HBReverseProxyResource
from protocols.http import HBProxyMgmtRedisSubscriberFactory
from protocols.http import HBProxyMgmtProtocolFactory

logging.config.dictConfig(Common.LOGGING)
logger = logging.getLogger("proxy")


class HBProxyServer(object):

    def __init__(self, bind_address, protocols, upstream_host, upstream_port,
                 redis_mgmt, redis_host, redis_port, request_channel,
                 response_channel, tcp_mgmt, tcp_mgmt_address, tcp_mgmt_port,
                 plugins):

        self.bind_address = bind_address
        self._start_logging()
        self.protocols = protocols
        self.upstream_host = upstream_host
        self.upstream_port = upstream_port
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.request_channel = request_channel
        self.response_channel = response_channel
        self.tcp_mgmt_address = tcp_mgmt_address
        self.tcp_mgmt_port = tcp_mgmt_port

        self.module_registry = Registry(plugins)
        self.site = server.Site(proxy.ReverseProxyResource(self.upstream_host,
                                self.upstream_port, ''))

        self.mgmt_protocol_factory = HBProxyMgmtProtocolFactory(self)
        reactor.listenTCP(self.tcp_mgmt_port, self.mgmt_protocol_factory,
                          interface=self.tcp_mgmt_address)

        redis_endpoint = TCP4ClientEndpoint(reactor, self.redis_host,
                                            self.redis_port)

        op_factory = RedisOperationFactory(self, redis_endpoint,
                                           self.response_channel)
        self.redis_conn = redis_endpoint.connect(
            HBProxyMgmtRedisSubscriberFactory(self.request_channel,
                                              op_factory))
        self.redis_conn.addCallback(self.subscribe).addCallback(
            self.start_proxy)


    def _start_logging(self):
        self.observer = log.PythonLoggingObserver(loggerName="proxy")
        self.observer.start()
        logger.info("started twisted logging observer")

    def start_proxy(self, result):
        resource = HBReverseProxyResource(self.upstream_host,
                                          self.upstream_port, '',
                                          self.module_registry)
        f = server.Site(resource)
        f.requestFactory = HBReverseProxyRequest
        self.protocol = self.protocols['http']
        self.proxy = reactor.listenTCP(self.protocol, f,
                                       interface=self.bind_address)
        log.msg("Proxy Started")
        return self.proxy

    def subscribe(self, redis):
        return redis.subscribe()

    def run(self):
        reactor.run()

    def _stop_test(self, result):
        reactor.stop()

    def test(self):
        self.tests = self.module_registry.test()
        self.tests.addCallback(self._stop_test)
        self.tests.callback("start test")
        reactor.run()



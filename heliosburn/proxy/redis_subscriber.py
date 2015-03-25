
from twisted.internet import reactor
from twisted.python import log
from twisted.internet import protocol
from twisted.internet import defer
from txredis.client import RedisClientFactory
from txredis.client import RedisClient
from txredis.client import RedisSubscriber
from twisted.trial import unittest


class HBRedisMessageHandler(object):

    def __init__(self, message, **configs):
        self.message = message
        self.configs = configs
        self.log = log

    def execute(self):
        pass


class HBRedisMessageHandlerFactory(object):
    message_handler = HBRedisMessageHandler

    def __init__(self, message_handler=None, **configs):
        self.message_handler = message_handler
        self.configs = configs

    def get_handler(self, message):
        return self.message_handler(message, **self.configs)


class HBRedisTestMessageHandler(HBRedisMessageHandler):

    def __init__(self, message, deferred, **configs):
        HBRedisMessageHandler.__init__(self, message, **configs)
        self.deferred = deferred

    def execute(self):
        self.deferred.callback(self.message)


class HBRedisTestMessageHandlerFactory(HBRedisMessageHandlerFactory,
                                       unittest.TestCase):
    message_handler = HBRedisTestMessageHandler

    def __init__(self,
                 response_handler,
                 fail_handler,
                 message_handler=None,
                 **configs):
        HBRedisMessageHandlerFactory.__init__(self,
                                              **configs)
        self.message_handler = HBRedisTestMessageHandler
        self.f_deferred = defer.Deferred()
        self._test_response = response_handler
        self._test_failed = fail_handler

    def get_handler(self, message):
        self.m_deferred = defer.Deferred()
        self.m_deferred.addCallback(self._test_response)
        self.m_deferred.addErrback(self._test_failed)
        self.m_deferred.addCallback(self._message_handled)
        return self.message_handler(message,
                                    self.m_deferred,
                                    **self.configs)

    def _message_handled(self, message):
        self.f_deferred.callback(message)

    def get_deferred(self):
        return self.f_deferred


class HBRedisSubscriber(RedisSubscriber):

    def __init__(self, channel, handler_factory, *args, **kwargs):
        RedisSubscriber.__init__(self, *args, **kwargs)
        self.channel = channel
        self.handler_factory = handler_factory
        self.status = "initialized"

    def subscribe(self):
        self.s_deferred = defer.Deferred()
        super(HBRedisSubscriber, self).subscribe(self.channel)
        self.status = "subscribed"
        return self.s_deferred

    def unsubscribe(self):
        self.u_deferred = defer.Deferred()
        super(HBRedisSubscriber, self).unsubscribe(self.channel)
        self.status = "unsubscribed"
        return self.u_deferred

    def messageReceived(self, channel, message):
        handler = self.handler_factory.get_handler(message)
        handler.execute()

    def channelSubscribed(self, channel, numSubscriptions):
        self.status = "subscribed to channel: " + channel
        self.s_deferred.callback(self.status)

    def channelUnsubscribed(self, channel, numSubscriptions):
        self.status = "unsubscribed from channel: " + channel
        self.u_deferred.callback(self.status)


class HBRedisSubscriberFactory(protocol.Factory):

    def __init__(self, request_channel, handler_factory):
        self.request_channel = request_channel
        self.handler_factory = handler_factory

    def buildProtocol(self, addr):
        return HBRedisSubscriber(self.request_channel,
                                 self.handler_factory)

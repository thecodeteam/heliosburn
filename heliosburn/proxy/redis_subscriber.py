
from twisted.internet import reactor
from twisted.python import log
from twisted.internet import protocol
from twisted.internet import defer
from txredis.client import RedisClientFactory
from txredis.client import RedisClient
from txredis.client import RedisSubscriber


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


class HBRedisSubscriber(RedisSubscriber):

    def __init__(self, channel, handler_factory, *args, **kwargs):
        RedisSubscriber.__init__(self, *args, **kwargs)
        self.channel = channel
        self.handler_factory = handler_factory

    def subscribe(self):
        self.subscribed = defer.Deferred()
        print("subscriber_subscribe")
        super(HBRedisSubscriber, self).subscribe(self.channel)
        return self.subscribed

    def unsubscribe(self):
        super(HBRedisSubscriber, self).unsubscribe(self.channel)

    def messageReceived(self, channel, message):
        handler = self.handler_factory.get_handler(message)
        handler.execute()

    def log_msg(self, message):
        log.msg(message)

    def channelSubscribed(self, channel, numSubscriptions):

        message = "Subscribed to channel: "
        message += channel
        message += " there are now : "
        message += str(numSubscriptions)
        message += " subscribers "

        self.subscribed.addCallback(self.log_msg)
        self.subscribed.callback(message)

    def channelUnsubscribed(self, channel, numSubscriptions):
        log.msg("Unsubscribed from channel: "
                + channel
                + " there are : "
                + str(numSubscriptions)
                + " subscribers remaining ")


class HBRedisSubscriberFactory(protocol.Factory):

    def __init__(self, request_channel, handler_factory):
        self.request_channel = request_channel
        self.handler_factory = handler_factory

    def buildProtocol(self, addr):
        return HBRedisSubscriber(self.request_channel,
                                 self.handler_factory)

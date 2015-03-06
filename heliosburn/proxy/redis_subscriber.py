
from twisted.internet import reactor
from twisted.python import log
from twisted.internet import protocol
from txredis.client import RedisClientFactory
from txredis.client import RedisClient
from txredis.client import RedisSubscriber


class HBRedisMessageHandler(object):

    def __init__(self, message):
        self.message = message

    def execute(self):
        pass


class HBRedisMessageHandlerFactory(object):
    message_handler = HBRedisMessageHandler

    def __init__(self, message_handler=None):
        self.message_handler = message_handler

    def get_handler(self, message):
        return self.message_handler(message)


class HBRedisSubscriber(RedisSubscriber):

    def __init__(self, channel, handler_factory, *args, **kwargs):
        RedisSubscriber.__init__(self, *args, **kwargs)
        self.channel = channel
        self.handler_factory = handler_factory

    def subscribe(self):
        super(HBRedisSubscriber, self).subscribe(self.channel)

    def unsubscribe(self):
        super(HBRedisSubscriber, self).unsubscribe(self.channel)

    def messageReceived(self, channel, message):
        handler = self.handler_factory.get_handler(message)
        handler.execute()

    def channelSubscribed(self, channel, numSubscriptions):
        log.msg("Subscribed to channel: "
                + channel
                + " it is subscriber 1 of : "
                + str(numSubscriptions))

    def channelUnSubscribed(self, channel, numSubscriptions):
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

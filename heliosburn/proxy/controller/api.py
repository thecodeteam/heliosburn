
import json
from txredis.client import RedisClientFactory
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet import server
from protocols import HBReverseProxyRequest
from protocols import HBReverseProxyResource


class OperationResponse(object):

    def __init__(self, code, message, key):

        self.deferred = defer.Deferred()
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

    def getDeferred(self):
        return self.deferred


class RedisOperationResponse(OperationResponse):

    def __init__(self, code, message, key, redis_endpoint=None,
                 response_channel=None):

        OperationResponse.__init__(self, code, message, key)

        self.response_channel = response_channel

        self.redis_conn = redis_endpoint.connect(RedisClientFactory())
        self.redis_conn.addCallback(self.set_redis_client)

    def set_redis_client(self, redis_client):
        self.redis_client = redis_client

    def _send(self, result):
        self.redis_client.publish(self.response_channel,
                                  json.dumps(self.response))
        self.redis_client.set(self.response['key'], self.response)

    def send(self):
        self.redis_conn.addCallback(self._send)


class OperationResponseFactory(object):

    def get_response(self, code, message, key):
        response = OperationResponse(code,
                                     message,
                                     key)
        return response


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


class OperationFactory(object):

    def __init__(self, controller):
        self.controller = controller
        self.response_factory = OperationResponseFactory()

    def get_operation(self, message):
        op_string = json.loads(message)
        operation = None

        if "stop" == op_string['operation']:
            operation = StopProxy(self.controller,
                                  self.response_factory,
                                  op_string['key'])

        if "start" == op_string['operation']:
            operation = StartProxy(self.controller,
                                   self.response_factory,
                                   op_string['key'])

        if "stop_recording" == op_string['operation']:
            operation = StopRecording(self.controller,
                                      self.response_factory,
                                      op_string['key'],
                                      recording_id=op_string['param'])

        if "start_recording" == op_string['operation']:
            operation = StartRecording(self.controller,
                                       self.response_factory,
                                       op_string['key'],
                                       recording_id=op_string['param'])

        if "reload" == op_string['operation']:
            operation = ReloadPlugins(self.controller,
                                      self.response_factory,
                                      op_string['key'])

        if "reset" == op_string['operation']:
            operation = ResetPlugins(self.controller,
                                     self.response_factory,
                                     op_string['key'])

        if "upstream_port" == op_string['operation']:
            operation = ChangeUpstreamPort(self.controller,
                                           self.response_factory,
                                           op_string['key'],
                                           new_port=op_string['param'])

        if "upstream_host" == op_string['operation']:
            operation = ChangeUpstreamHost(self.controller,
                                           self.response_factory,
                                           op_string['key'],
                                           new_host=op_string['param'])

        if "bind_address" == op_string['operation']:
            self.controller.bind_address = op_string['param']
            operation = ChangeBindAddress(self.controller,
                                          self.response_factory,
                                          op_string['key'])

        if "bind_port" == op_string['operation']:
            self.controller.protocol = op_string['param']
            operation = ChangeBindPort(self.controller,
                                       self.response_factory,
                                       op_string['key'])

        if "test" == op_string['operation']:
            operation = RunTest(self.controller,
                                self.response_factory,
                                op_string['key'],
                                module_name=op_string['param'])

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


class ControllerOperation(object):

    def __init__(self, controller, response_factory, key):
        self.controller = controller
        self.operation = defer.Deferred()
        self.response = response_factory.get_response(200,
                                                      "execution successful",
                                                      key)
        self.key = key

    def execute(self):
        return self.operation.callback(self.response)

    def respond(self, result):
        self.response.send()

    def addCallback(self, callback):
        return self.operation.addCallback(callback)


class StopProxy(ControllerOperation):

    def __init__(self, controller, response_factory, key):
        ControllerOperation.__init__(self, controller, response_factory, key)

        self.addCallback(self.stop)
        self.addCallback(self.respond)

    def stop(self, result):
        deferred = self.controller.proxy.stopListening()
        self.response.set_message("stop " + self.response.get_message())

        return deferred


class StartProxy(ControllerOperation):

    def __init__(self, controller, response_factory, key):

        ControllerOperation.__init__(self, controller, response_factory, key)

        self.addCallback(self.start)
        self.addCallback(self.respond)

    def start(self, result):
        resource = HBReverseProxyResource(self.controller.upstream_host,
                                          self.controller.upstream_port, '',
                                          self.controller.module_registry)
        f = server.Site(resource)
        f.requestFactory = HBReverseProxyRequest
        protocol = self.controller.protocol
        bind_address = self.controller.bind_address
        self.controller.proxy = reactor.listenTCP(protocol, f,
                                                  interface=bind_address)
        self.response.set_message("start " + self.response.get_message())

        return self.controller.proxy


class ChangeUpstreamPort(ControllerOperation):

    def __init__(self, controller, response_factory, key, new_port):
        ControllerOperation.__init__(self, controller, response_factory, key)
        controller.upstream_port = new_port
        stop_op = StopProxy(controller, response_factory, key)
        self.start_op = StartProxy(controller, response_factory, key)

        d = self.addCallback(stop_op.stop).addCallback(self.start_op.start)
        d.addCallback(self.update_message)
        d.addCallback(self.respond)

    def update_message(self, result):
        self.response.set_message({'Change_upstream_port':
                                  [self.response.get_message()]
                                   })


class ChangeUpstreamHost(ControllerOperation):

    def __init__(self, controller, response_factory, key, new_host):
        ControllerOperation.__init__(self, controller, response_factory, key)
        controller.upstream_host = new_host
        stop_op = StopProxy(controller, response_factory, key)
        self.start_op = StartProxy(controller, response_factory, key)

        d = self.addCallback(stop_op.stop).addCallback(self.start_op.start)
        d.addCallback(self.update_message)
        d.addCallback(self.respond)

    def update_message(self, result):
        self.response.set_message({'Change_upstream_host':
                                  [self.response.get_message()]
                                   })


class ChangeBindAddress(ControllerOperation):

    def __init__(self, controller, response_factory, key):
        ControllerOperation.__init__(self, controller, response_factory, key)
        stop_op = StopProxy(controller, response_factory, key)
        self.start_op = StartProxy(controller, response_factory, key)

        d = self.addCallback(stop_op.stop).addCallback(self.start_op.start)
        d.addCallback(self.update_message)
        d.addCallback(self.respond)

    def update_message(self, result):
        self.response.set_message({'Change_bind_address':
                                  [self.response.get_message()]
                                   })


class ChangeBindPort(ControllerOperation):

    def __init__(self, controller, response_factory, key):
        ControllerOperation.__init__(self, controller, response_factory, key)
        stop_op = StopProxy(controller, response_factory, key)
        self.start_op = StartProxy(controller, response_factory, key)

        d = self.addCallback(stop_op.stop).addCallback(self.start_op.start)
        d.addCallback(self.update_message)
        d.addCallback(self.respond)

    def update_message(self, result):
        self.response.set_message({'Change_bind_port':
                                  [self.response.get_message()]
                                   })


class StopRecording(ControllerOperation):

    def __init__(self, controller, response_factory, key, **params):
        ControllerOperation.__init__(self, controller, response_factory, key)

        self.params = params

        d = self.addCallback(self.stop_recording)
        d.addCallback(self.respond)

    def stop_recording(self, result):
        self.controller.module_registry.stop(module_name='TrafficRecorder',
                                             **self.params)
        self.response.set_message("Stopped Recording: { "
                                  + self.response.get_message() + ", "
                                  + "}")


class StartRecording(ControllerOperation):

    def __init__(self, controller, response_factory, key, **params):
        ControllerOperation.__init__(self, controller, response_factory, key)

        self.params = params

        d = self.addCallback(self.start_recording)
        d.addCallback(self.respond)

    def start_recording(self, result):
        self.controller.module_registry.start(module_name='TrafficRecorder',
                                              **self.params)
        self.response.set_message({'Started Recording':
                                   [self.response.get_message()]
                                   })


class ResetPlugins(ControllerOperation):

    def __init__(self, controller, response_factory, key):
        ControllerOperation.__init__(self, controller, response_factory, key)
        stop_op = StopProxy(controller, response_factory, key)
        self.start_op = StartProxy(controller, response_factory, key)

        d = self.addCallback(stop_op.stop)
        d = d.addCallback(self.start_op.start)
        d.addCallback(self.reset_plugins)
        d.addCallback(self.update_message)
        d.addCallback(self.respond)

    def reset_plugins(self, result):
        self.controller.module_registry.reset()

    def update_message(self, result):
        self.response.set_message({'Reset_plugins':
                                  [self.response.get_message()]
                                   })


class ReloadPlugins(ControllerOperation):

    def __init__(self, controller, response_factory, key):
        ControllerOperation.__init__(self, controller, response_factory, key)
        stop_op = StopProxy(controller, response_factory, key)
        self.start_op = StartProxy(controller, response_factory, key)

        d = self.addCallback(stop_op.stop)
        d = d.addCallback(self.start_op.start)
        d.addCallback(self.reload_plugins)
        d.addCallback(self.update_message)
        d.addCallback(self.respond)

    def reload_plugins(self, result):
        self.controller.module_registry.reload()

    def update_message(self, result):
        self.response.set_message({'Reload_plugins':
                                  [self.response.get_message()]
                                   })


class RunTest(ControllerOperation):

    def __init__(self, controller, response_factory, key, module_name):
        ControllerOperation.__init__(self, controller, response_factory, key)
        self.module_name = module_name

        c_port_op = ChangeUpstreamPort(controller,
                                       response_factory,
                                       key,
                                       7599)

        c_host_op = ChangeUpstreamHost(controller,
                                       response_factory,
                                       key,
                                       '127.0.0.1')
        d = self.addCallback(self.run_test)
        d.addCallback(self.respond)

    def run_test(self, result):
        self.controller.module_registry.test(module_name=self.module_name)
        self.response.set_message({'test started':
                                   [self.response.get_message()]
                                   })

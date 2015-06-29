
import json
from txredis.client import RedisClientFactory
from twisted.internet import defer
from twisted.internet import reactor
from twisted.web import server
from twisted.python import log
from protocols.http import HBReverseProxyRequest
from protocols.http import HBReverseProxyResource
from models import SessionModel


class OperationResponse(object):

    def __init__(self, code, message, key):

        self.deferred = defer.Deferred()
        self.response = {'code': code,
                         'message': [message],
                         'key': key
                         }

    def get_code(self):
        return self.response['code']

    def get_message(self):
        return str(self.response['message'])

    def set_code(self, code):
        self.response['code'] = code

    def set_message(self, message):
        self.response['message'] = []
        self.response['message'].append(message)

    def add_message(self, message):
        self.response['message'].append(message)

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
        self.redis_client.set(self.response['key'],
                              json.dumps(self.response))
        log.msg("Response posted to redis key: " + self.response['key'])

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

        if "stop_session" == op_string['operation']:
            operation = StopSession(self.controller,
                                    self.response_factory,
                                    op_string['key'],
                                    recording_id=op_string['param'])

        if "start_session" == op_string['operation']:
            operation = StartSession(self.controller,
                                     self.response_factory,
                                     op_string['key'],
                                     session_id=op_string['param'])

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
            self.controller.proxy_address = op_string['param']
            operation = ChangeBindAddress(self.controller,
                                          self.response_factory,
                                          op_string['key'])

        if "bind_port" == op_string['operation']:
            self.controller.proxy_port = op_string['param']
            operation = ChangeBindPort(self.controller,
                                       self.response_factory,
                                       op_string['key'])

        if "test" == op_string['operation']:
            operation = RunTest(self.controller,
                                self.response_factory,
                                op_string['key'],
                                module_name=op_string['param']['module'],
                                response_file=op_string['param']['response'])

        if "status" == op_string['operation']:
            operation = Status(self.controller,
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


class ServerOperation(object):

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


class StopProxy(ServerOperation):

    def __init__(self, controller, response_factory, key):
        ServerOperation.__init__(self, controller, response_factory, key)

        self.addCallback(self.stop)
        self.addCallback(self.respond)

    def stop(self, result):
        deferred = self.controller.proxy.stopListening()
        self.response.set_message("stop " + self.response.get_message())

        return deferred


class StartProxy(ServerOperation):

    def __init__(self, controller, response_factory, key):

        ServerOperation.__init__(self, controller, response_factory, key)

        self.addCallback(self.start)
        self.addCallback(self.respond)

    def start(self, result):
        resource = HBReverseProxyResource(self.controller.upstream_host,
                                          self.controller.upstream_port, '',
                                          self.controller.module_registry)
        f = server.Site(resource)
        f.requestFactory = HBReverseProxyRequest
        proxy_port = self.controller.proxy_port
        proxy_address = self.controller.proxy_address
        self.controller.proxy = reactor.listenTCP(proxy_port, f,
                                                  interface=proxy_address)
        self.response.set_message("start " + self.response.get_message())

        return self.controller.proxy


class ChangeUpstreamPort(ServerOperation):

    def __init__(self, controller, response_factory, key, new_port):
        ServerOperation.__init__(self, controller, response_factory, key)
        stop_op = StopProxy(controller, response_factory, key)
        start_op = StartProxy(controller, response_factory, key)

        self.new_port = new_port
        controller.upstream_port = new_port
        d = self.addCallback(stop_op.stop).addCallback(start_op.start)
        d.addCallback(self.update)
        d.addCallback(self.respond)

    def update(self, result):
        self.response.set_message({'Change_upstream_port':
                                  [self.response.get_message()]
                                   })
        log.msg("Upstream port changed to: " + str(self.new_port))


class ChangeUpstreamHost(ServerOperation):

    def __init__(self, controller, response_factory, key, new_host):
        ServerOperation.__init__(self, controller, response_factory, key)
        self.new_host = new_host
        controller.upstream_host = new_host
        stop_op = StopProxy(controller, response_factory, key)
        start_op = StartProxy(controller, response_factory, key)

        d = self.addCallback(stop_op.stop).addCallback(start_op.start)
        d.addCallback(self.update)
        d.addCallback(self.respond)

    def update(self, result):
        self.response.set_message({'Change_upstream_host':
                                  [self.response.get_message()]
                                   })
        log.msg("Upstream host changed to: " + str(self.new_host))


class ChangeBindAddress(ServerOperation):

    def __init__(self, controller, response_factory, key):
        ServerOperation.__init__(self, controller, response_factory, key)
        stop_op = StopProxy(controller, response_factory, key)
        start_op = StartProxy(controller, response_factory, key)

        d = self.addCallback(stop_op.stop).addCallback(start_op.start)
        d.addCallback(self.update_message)
        d.addCallback(self.respond)

    def update_message(self, result):
        self.response.set_message({'Change_bind_address':
                                  [self.response.get_message()]
                                   })


class ChangeBindPort(ServerOperation):

    def __init__(self, controller, response_factory, key):
        ServerOperation.__init__(self, controller, response_factory, key)
        stop_op = StopProxy(controller, response_factory, key)
        start_op = StartProxy(controller, response_factory, key)

        d = self.addCallback(stop_op.stop).addCallback(start_op.start)
        d.addCallback(self.update_message)
        d.addCallback(self.respond)

    def update_message(self, result):
        self.response.set_message({'Change_bind_port':
                                  [self.response.get_message()]
                                   })


class StopRecording(ServerOperation):

    def __init__(self, controller, response_factory, key, **params):
        ServerOperation.__init__(self, controller, response_factory, key)

        self.params = params

        d = self.addCallback(self.stop_recording)
        d.addCallback(self.respond)

    def stop_recording(self, result):
        self.controller.module_registry.stop(module_name='TrafficRecorder',
                                             **self.params)
        self.response.set_message("Stopped Recording: { " +
                                  self.response.get_message() + ", " + "}")


class StartRecording(ServerOperation):

    def __init__(self, controller, response_factory, key, **params):
        ServerOperation.__init__(self, controller, response_factory, key)

        self.params = params

        d = self.addCallback(self.start_recording)
        d.addCallback(self.respond)

    def start_recording(self, result):
        status = self.controller.module_registry.status(
            module_name='TrafficRecorder',
            **self.params)
        if status['state'] != "running":
            self.controller.module_registry.start(
                module_name='TrafficRecorder',
                **self.params)
            self.response.set_message({'Started Recording':
                                      [self.response.get_message()]})
        else:
            self.response.set_code(501)
            self.response.set_message({'Busy': status})


class StartSession(ServerOperation):

    def __init__(self, controller, response_factory, key, **params):
        ServerOperation.__init__(self, controller, response_factory, key)

        self.params = params
        session_id = params['session_id']
        self.session = SessionModel({"_id": session_id})
        controller.upstream_host = self.session["upstreamHost"]
        self.response.add_message("Upstream Host set to: " +
                                  str(controller.upstream_host))
        controller.upstream_port = self.session["upstreamPort"]
        self.response.add_message("Upstream Port set to: " +
                                  str(controller.upstream_port))
        stop_op = StopProxy(controller, response_factory, key)
        start_op = StartProxy(controller, response_factory, key)

        d = self.addCallback(stop_op.stop).addCallback(start_op.start)
        d.addCallback(self.start_session)
        d.addCallback(self.respond)

    def start_session(self, result):

        try:
            self.params['test_plan'] = self.session['testplan']['id']
            status = self.controller.module_registry.status(
                module_name='Injection',
                **self.params)
            if status['state'] != "running":
                self.controller.module_registry.start(
                    module_name='Injection',
                    **self.params)
            else:
                self.response.set_code(501)
                self.response.set_message({'Busy': status})
        except KeyError:
            pass

        try:
            profile_id = self.session['qosProfile']['id']
            self.params['profile_id'] = profile_id
            status = self.controller.module_registry.status(
                module_name='QOS',
                **self.params)
            if status['state'] != "running":
                self.controller.module_registry.start(
                    module_name='QOS',
                    **self.params)
            else:
                self.response.set_code(501)
                self.response.set_message({'Busy': status})
        except KeyError:
            pass

        try:
            profile_id = self.session['serverOverloadProfile']['id']
            self.params['profile_id'] = profile_id
            status = self.controller.module_registry.status(
                module_name='ServerOverload',
                **self.params)

            if status['state'] != "running":
                self.controller.module_registry.start(
                    module_name='ServerOverload',
                    **self.params)
            else:
                self.response.set_code(501)
                self.response.set_message({'Busy': status})
        except KeyError:
            pass

        self.response.set_message({'Started Injection Session':
                                  [self.response.get_message()]})


class StopSession(ServerOperation):

    def __init__(self, controller, response_factory, key, **params):
        ServerOperation.__init__(self, controller, response_factory, key)

        self.params = params

        d = self.addCallback(self.stop_session)
        d.addCallback(self.respond)

    def stop_session(self, result):
        self.controller.module_registry.stop(module_name='Injection',
                                             **self.params)
        self.controller.module_registry.stop(module_name='QOS',
                                             **self.params)
        self.controller.module_registry.stop(module_name='ServerOverload',
                                             **self.params)
        self.response.set_message("Stopped Injection Session: { " +
                                  self.response.get_message() + ", " + "}")
#        stop_op = StopProxy(controller, response_factory, key)


class ResetPlugins(ServerOperation):

    def __init__(self, controller, response_factory, key):
        ServerOperation.__init__(self, controller, response_factory, key)
        stop_op = StopProxy(controller, response_factory, key)
        start_op = StartProxy(controller, response_factory, key)

        d = self.addCallback(stop_op.stop)
        d = d.addCallback(start_op.start)
        d.addCallback(self.reset_plugins)
        d.addCallback(self.update_message)
        d.addCallback(self.respond)

    def reset_plugins(self, result):
        self.controller.module_registry.reset()

    def update_message(self, result):
        self.response.set_message({'Reset_plugins':
                                  [self.response.get_message()]
                                   })


class ReloadPlugins(ServerOperation):

    def __init__(self, controller, response_factory, key):
        ServerOperation.__init__(self, controller, response_factory, key)
        stop_op = StopProxy(controller, response_factory, key)
        start_op = StartProxy(controller, response_factory, key)

        d = self.addCallback(stop_op.stop)
        d = d.addCallback(start_op.start)
        d.addCallback(self.reload_plugins)
        d.addCallback(self.update_message)
        d.addCallback(self.respond)

    def reload_plugins(self, result):
        self.controller.module_registry.reload()

    def update_message(self, result):
        self.response.set_message({'Reload_plugins':
                                  [self.response.get_message()]
                                   })


class RunTest(ServerOperation):

    def __init__(self,
                 server,
                 response_factory,
                 key,
                 module_name,
                 response_file):
        ServerOperation.__init__(self, server, response_factory, key)
        self.module_name = module_name
        self.response_file = response_file
        self.server = server
        self.response_factory = response_factory
        self.key = key
        self.orig_upstream_host = server.upstream_host
        self.orig_upstream_port = server.upstream_port

        d = self._connect_echo_server()
        d.addCallback(self.run_test)
        d.addCallback(self.respond)
        d.addCallback(self._disconnect_echo_server)

    def run_test(self, result):
        tests = self.controller.module_registry.test(
            module_name=self.module_name, response_file=self.response_file)
        self.response.set_message({'test started':
                                   [self.response.get_message()]
                                   })
        tests.callback(self.response)

    def _connect_echo_server(self):
        self.server.upstream_host = '127.0.0.1'
        self.server.upstream_port = 7599
        stop_op = StopProxy(self.server, self.response_factory, self.key)
        start_op = StartProxy(self.server, self.response_factory, self.key)

        log.msg("Upstream host changed to echo server: " +
                str(self.server.upstream_host) +
                ":" + str(self.server.upstream_port))

        return self.addCallback(stop_op.stop).addCallback(start_op.start)

    def _disconnect_echo_server(self, unused):
        self.server.upstream_host = self.orig_upstream_host
        self.server.upstream_port = self.orig_upstream_port
        stop_op = StopProxy(self.server, self.response_factory, self.key)
        start_op = StartProxy(self.server, self.response_factory, self.key)

        log.msg("Upstream host changed to previous server: " +
                str(self.server.upstream_host) +
                ":" + str(self.server.upstream_port))

        return self.addCallback(stop_op.stop).addCallback(start_op.start)


class Status(ServerOperation):

    def __init__(self, controller, response_factory, key, module_name):
        ServerOperation.__init__(self, controller, response_factory, key)
        self.module_name = module_name

        d = self.addCallback(self.get_status)
        d.addCallback(self.respond)

    def get_status(self, result):
        status = self.controller.module_registry.status(
            module_name=self.module_name)
        self.response.set_message({'status': status})

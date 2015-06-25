import redis
import modules
import json
import datetime
import pymongo
import time
from multiprocessing import Process
from zope.interface import implements
from zope.interface import Interface
from twisted.internet import defer
from twisted.plugin import IPlugin
from twisted.plugin import getPlugins
from twisted.python import log
from twisted.trial import unittest
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor
from twisted.web import server
from twisted.web import resource
from protocols.redis import HBRedisSubscriberFactory
from protocols.redis import HBRedisTestMessageHandlerFactory


class HBProxyEchoServer(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        response = self._get_response()
        log.msg("EchoServer: Sent response:\n " + response)
        return response

    def _get_response(self):
        if self.response_file is None:
            with open("proxy/default.asis", 'r+') as data:
                    response = data.read()
        else:
            with open("proxy/" + self.response_file, 'r+') as data:
                    response = data.read()
        return response

    def set_response(self, response_file):
        self.response_file = response_file


class IModule(Interface):
    """
    Module interface defined for proxy modules.

    .run() is called in every (defined) context.

    Currently implemented contexts:
        'request'
        'response'
    """

    def get_name(self):
        """
        Returns the unique name of the module
        @rtype: C{string}
        """

    def handle_request(self):
        """
        Called to handle proxy request event
        """

    def handle_response(self):
        """
        Called to handle proxy response event
        """

    def reset(self, **keywords):
        """
        If the module maintains state, this method is called to reset
        the current state of the module

        """

    def reload(self, **keywords):
        """
        this method is called to reload the module configuration
        """

    def configure(self, **configs):
        """
        this method is called to provide configuration data to the
        module
        """

    def start(self, **keywords):
        """
        this method is called to start the module execution
        """

    def stop(self, **keywords):
        """
        this method is called to stop the module execution
        """


class AbstractModule(object):
    implements(IPlugin, IModule)

    """
    Base class used to implement a twisted plugin based IModule interface.

    """

    def __init__(self):
        """
        Initialization of a proxy module instance
        """

        self.session_id = None
        self.profile_id = None
        self.name = self.__class__.__name__
        self.log = log
        self.state = "loaded"
        self.status = str(datetime.datetime.now())
        self.stats = {}

    def get_name(self):
        """
        Returns the unique name of the module
        """
        return self.name

    def set_log(self, log):
        self.log = log

    def log(self):
        return self.log

    def handle_request(self, request):
        """
        Called by to handle proxy request event
        """
        return request

    def handle_response(self, response):
        """
        Called to handle proxy response event
        """
        return response

    def reset(self):
        """
        If the module maintains state, this method is called to reset
        the current state of the module
        """

    def reload(self):
        """
        this method is called to reload the module configuration
        """

    def configure(self, **configs):
        """
        this method is called to provide configuration data to the
        module
        """

    def start(self, **params):
        """
        this method is called to start the module execution
        """
        self.state = "running"
        self.status = str(datetime.datetime.now())

    def stop(self, **params):
        """
        this method is called to stop the module execution
        """
        self.state = "stopped"
        self.status = str(datetime.datetime.now())

    def test(self, module_name=None):
        """
        this method is called to run the module(s) tests
        """

    def get_state(self):
        """
        this method is called to  get the module(s) current state
        """
        return self.state

    def get_status(self):
        """
        this method is called to get the module(s) current status
        """
        return self.status

    def store_stats(self):
        if self.get_stats():
            conn = pymongo.MongoClient()
            db = conn.proxy
            db.statistics.insert(self.get_stats())

    def get_stats(self):
        """
        this method is called to get the module(s) current running statistics
        """
        self.stats['session_id'] = self.session_id
        self.stats['profile_id'] = self.profile_id
        return self.stats

    def isStarted(self):
        if self.state == "running":
            return True
        else:
            return False


class AbstractAPITestModule(AbstractModule, unittest.TestCase):
    implements(IPlugin, IModule)
    _testMethodName = "temp"

    def configure(self, **configs):
        self.redis_host = configs['redis_host']
        self.redis_port = configs['redis_port']
        self.redis_db = configs['redis_db']
        self.redis_pub_queue = configs['traffic_pub_queue']
        self.redis_sub_queue = configs['traffic_sub_queue']
        self.redis_client = redis.StrictRedis(host=self.redis_host,
                                              port=self.redis_port,
                                              db=self.redis_db)

    def start(self, options):
        handler_factory = HBRedisTestMessageHandlerFactory(self.evaluate,
                                                           self._failure)

        self.redis_endpoint = TCP4ClientEndpoint(reactor,
                                                 self.redis_host,
                                                 self.redis_port)
        self.channel = self.redis_sub_queue
        d = self.redis_endpoint.connect(HBRedisSubscriberFactory(self.channel,
                                        handler_factory))

        sub_d = d.addCallback(self._subscribe)
        sub_d.addErrback(self._error)

        pub_d = sub_d.addCallback(self._publish_message)
        pub_d.addErrback(self._error)

        handler_d = handler_factory.get_deferred()
        handler_d.addCallback(self._unsubscribe)
        handler_d.addErrback(self._error)

        return handler_d

    def evaluate(self, result):
        response = json.loads(result)
        result = self.assertEqual(self.get_expected(), response)
        success_message = self.__class__.__name__ + ": "
        success_message += "SUCCESS!\n"
        success_message += "Result: " + str(result)
        print(success_message)

    def get_expected(self):
        message = "get_expected not implemented by child class"
        raise NotImplementedError(message)

    def get_message(self):
        message = "get_message not implemented by child class"
        raise NotImplementedError(message)

    def _error(self, failure):
        print(failure)

    def _subscribe(self, redis):
        self.redis_subscriber = redis
        return redis.subscribe()

    def _unsubscribe(self, result):
        return self.redis_subscriber.unsubscribe()

    def _failure(self, failure):
        result = failure.getErrorMessage()
        fail_message = self.__class__.__name__ + ": "
        fail_message += "FAILED!\n"
        fail_message += "Result: " + str(result)
        print(fail_message)

    def _get_operation_message(self, operation, param, key):

        message = {}
        message['operation'] = operation
        message['param'] = param
        message['key'] = key

        return message

    def _publish_message(self, result):
        message = self.get_message()
        if message:
            self.redis_client.publish(self.redis_pub_queue, message)
        return result


class Registry(object):

    def __init__(self, configs):
        self.configs = configs
        self.session_modules = configs['plugins']['session']
        self.support_modules = configs['plugins']['support']
        self.test_modules = configs['plugins']['test']
        self.echo_server_port = configs['echo_server_port']
        self.test_mode = False

        self.plugins = {plugin.get_name(): plugin for plugin in
                        getPlugins(IModule, modules)}

        self._load_session_modules()
        self._load_support_modules()
        self._load_test_modules()
        p = Process(target=self._dump_stats)
        p.start()

    def _load_session_modules(self):
        for module in self.session_modules:
            name = module
            self.plugins[name].configure(**self.configs)
            log.msg(name + " loaded into proxy session pipeline")

    def _load_support_modules(self):
        for module in self.support_modules:
            name = module
            self.plugins[name].configure(**self.configs)
            log.msg("Proxy support module: " + name + " loaded")

    def _load_test_modules(self):
        for module in self.test_modules:
            name = module
            self.plugins[name].configure(**self.configs)
            log.msg(name + " loaded into proxy test pipeline")

    def _build_request_pipeline(self):

        pipeline = defer.Deferred()

        for module in self.session_modules:
            module_name = module
            if self.plugins[module_name].isStarted():
                pipeline.addCallback(self.plugins[module_name].handle_request)

        return pipeline

    def _build_response_pipeline(self):

        pipeline = defer.Deferred()
        for module in self.session_modules:
            module_name = module
            if self.plugins[module_name].isStarted():
                pipeline.addCallback(self.plugins[module_name].handle_response)

        return pipeline

    def _test_mode_on(self, ignored):
        self.test_mode = True
        self.pipeline_modules = self.test_modules
        log.msg("Test mode: on")

    def _test_mode_off(self, ignored):
        self.test_mode = False
        self.session_modules = self.configs['plugins']['session']
        self.test_modules = self.configs['plugins']['test']
        log.msg("Test mode: off")
        self._stop_echo_server()

    def _start_echo_server(self, response_file=None):
        echo_resource = HBProxyEchoServer()
        echo_resource.set_response(response_file)

        echo_site = server.Site(echo_resource)
        self.echo_server = reactor.listenTCP(self.echo_server_port, echo_site)

        log.msg("Echo Server Started")

    def _stop_echo_server(self):
        self.echo_server.stopListening()
        log.msg("Echo Server Stopped")

    def _dump_stats(self):
        while True:
            for plugin in self.plugins.values():
                p = Process(target=plugin.store_stats)
                p.start()
                log.msg("Started recording stats for module: " + plugin.name)

            time.sleep(60)

    def handle_request(self, request, callback):

        """
        Executes the handle_request method of all currently active modules
        """
        pipeline = self._build_request_pipeline()
        pipeline.addCallback(callback)

        pipeline.callback(request)

    def handle_response(self, response, callback):

        """
        Executes the handle_response method of all currently active modules
        """
        pipeline = self._build_response_pipeline()
        pipeline.addCallback(callback)

        pipeline.callback(response)

    def reset(self):

        """
        Executes the reset method of all currently active modules
        """
        for plugin in self.plugins.values():
            plugin.reset()
            log.msg("Reseting module: " + plugin.name)

    def reload(self):

        """
        Executes the reload method of all currently active modules
        """
        for plugin in self.plugins.values():
            log.msg("Reloading module: " + plugin.name)
            plugin.reload()

    def start(self, module_name=None, **params):

        """
        Executes the start method of all or one currently active modules
        """
        if module_name:
            self.plugins[module_name].start(**params)
            log.msg("Starting  module: " + module_name)
        else:
            for plugin in self.plugins.values():
                plugin.start(**params)
                log.msg("Starting module: " + plugin.name)

    def stop(self, module_name=None, **params):

        """
        Executes the stop method of all or one currently active modules
        """
        if module_name:
            self.plugins[module_name].stop(**params)
            log.msg("Stopping  module: " + module_name)
        else:
            for plugin in self.pipeline_modules.values():
                plugin.stop(**params)
                log.msg("Stopping module: " + plugin.name)

    def test(self, module_name=None, response_file=None):

        """
        Executes the start method of all test modules
        """

        self._start_echo_server(response_file)
        test_deferred = defer.Deferred()
        test_deferred.addCallback(self._test_mode_on)
        if module_name:
            self.test_modules = []
            test_module = {}
            test_module['name'] = module_name
            self.test_modules.append(test_module)
            test_deferred.addCallback(self.plugins[module_name].start)
        else:
            for module in self.test_modules:
                name = module['name']
                test_deferred.addCallback(self.plugins[name].start)
        test_deferred.addCallback(self._test_mode_off)
        return test_deferred

    def status(self, module_name=None, **params):

        """
        Executes the status method of all plugins
        """

        if module_name:
            status = {
                "module": module_name,
                "state": self.plugins[module_name].get_state(),
                "status": self.plugins[module_name].get_status(),
                "stats": self.plugins[module_name].get_status()
            }
        else:
            status = []
            for plugin in self.plugins.values():
                p_status = {
                    "module": plugin.get_name(),
                    "state": plugin.get_state(),
                    "status": str(plugin.get_status()),
                    "stats": str(plugin.get_status())
                }
                status.append(p_status)

        log.msg("Status retrieved: " + str(status))
        return status

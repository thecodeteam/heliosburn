import io
import sys
import collections
from zope.interface import implements
from zope.interface import Interface
from twisted.internet import defer
from twisted.plugin import IPlugin
from twisted.plugin import getPlugins
from twisted.plugin import pluginPackagePaths
from twisted.python import log
import modules

"""
Simple Interface to handling proxy requests and responses via class instances.
To use, make a new class that inherits ProxyModuleBase. Each context
represents a step in the proxy request or client response process.

"""


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

        self.name = self.__class__.__name__
        self.log = log

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

    def stop(self, **params):
        """
        this method is called to stop the module execution
        """


class Registry(object):

    def __init__(self, plugin_config):
        self.pipeline_modules = plugin_config['pipeline']
        self.support_modules = plugin_config['support']
        self.test_modules = plugin_config['test']
        log.msg("loaded pipline modules: %s" % self.pipeline_modules)

        self.plugins = {plugin.get_name(): plugin for plugin in
                        getPlugins(IModule, modules)}

        for module in self.pipeline_modules:
            name = module['name']
            configs = module['kwargs']
            self.plugins[name].configure(**configs)

        for module in self.support_modules:
            name = module['name']
            configs = module['kwargs']
            self.plugins[name].configure(**configs)

        for module in self.test_modules:
            name = module['name']
            configs = module['kwargs']
            self.plugins[name].configure(**configs)

        log.msg("loaded plugins: %s" % self.plugins.keys())

    def _build_request_pipeline(self):

        pipeline = defer.Deferred()
        for module in self.pipeline_modules:
            module_name = module['name']
            pipeline.addCallback(self.plugins[module_name].handle_request)

        return pipeline

    def _build_response_pipeline(self):

        pipeline = defer.Deferred()
        for module in self.pipeline_modules:
            module_name = module['name']
            pipeline.addCallback(self.plugins[module_name].handle_response)

        return pipeline

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

    def reload(self):

        """
        Executes the reload method of all currently active modules
        """
        for plugin in self.plugins.values():
            plugin.reload()

    def start(self, module_name=None, **params):

        """
        Executes the start method of all or one currently active modules
        """
        if module_name:
            self.plugins[module_name].start(**params)
        else:
            for plugin in self.plugins.values():
                plugin.start(**params)

    def stop(self, module_name=None, **params):

        """
        Executes the stop method of all or one currently active modules
        """
        if module_name:
            self.plugins[module_name].stop(**params)
        else:
            for plugin in self.pipeline_modules.values():
                plugin.stop(**params)

    def test(self, module_name=None):

        """
        Executes the start method of all or one currently active modules
        """
        d = defer.Deferred()
        if module_name:
            d.addCallback(self.plugins[module_name].run_tests())
        else:
            for module in self.test_modules:
                name = module['name']
                d.addCallback(self.plugins[name].run_tests())

        return d


from twisted.python import log
from twisted.plugin import getPlugins
from proxy.iproxymodule import IModule


class Registry(object):

    def __init__(self, modules_list):
        self.modules_list = modules_list
        self.modules = {}
        for module in getPlugins(IModule):
            self.modules[module.name] = module

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

    def run_plugins(self, context, request_object=None):
        """
        Runs all proxy modules in the order specified in config.yaml

        """
#       for module_dict in self.modules:
#           class_ = self._get_class(module_dict)
#           instance_ = class_(context=context,
#                              request_object=request_object,
#                              run_contexts=module_dict['run_contexts'])
#           instance_.run(**module_dict['kwargs'])



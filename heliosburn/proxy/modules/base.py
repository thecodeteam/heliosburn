"""
Simple Interface to handling proxy requests and responses via class instances.
To use, make a new class that inherits ProxyModuleBase. Each context
represents a step in the proxy request or client response process. 

"""



class ProxyModuleBase(object):
    """
    Base class used to implement ProxyModule interface.

    .run() is called in every (defined) context.

    Currently implemented contexts:
        'request'
        'response'
    """

    proxy_object = None
    proxy_request_object = None
    proxy_respone_object = None
    current_context = None

    def __init__(self, run_contexts=[], context=None,
                    request_object=None, response_object=None):
        """
        Initialization of ProxyModuleBase instance
        """
        from twisted.python import log
        self.log = log
        self.run_contexts = run_contexts
        self.context = context
        self.request_object = request_object
        self.response_object = response_object

    def onRequest(self, **keywords):
        """
        Called by .run() when instantiated with a run_context that includes
        'request'. 
        """
        self.log.msg("Request: %s" % keywords)

    def onStatus(self, **keywords):
        """
        Called by .run() when instantiated with a run_context that includes
        'status'. 
        """
        self.log.msg("Status: %s" % keywords)
    
    def onResponse(self, **keywords):
        """
        Called by .run() when instantiated with a run_context that includes
        'response'. 
        """
        self.log.msg("Response: %s" % keywords)

    def run(self, **keywords):
        """
        Called by run_modules() after a module has been loaded (instantiated).
        if a given (predefined) context is listed in 'run_contexts', the
        respective method is called.
        """
        options =   {
                    'request' : self.onRequest,
                    'status' : self.onStatus,
                    'response' : self.onResponse,
                    }
        if self.context in self.run_contexts:
            options[self.context](**keywords)
        else:
            self.log.msg("not my turn yet")



import io
from zope.interface import Interface, Attribute


"""
Simple Interface to handling proxy requests and responses via class instances.
To use, make a new class that inherits ProxyModuleBase. Each context
represents a step in the proxy request or client response process.

"""


class IModule(Interface):
    """
    Base class used to implement ProxyModule interface.

    .run() is called in every (defined) context.

    Currently implemented contexts:
        'request'
        'response'
    """

    def __init__(self, run_contexts=[], context=None,
                 request_object=None):
        """
        Initialization of ProxyModuleBase instance
        """
        from twisted.python import log

        self.name = "Interface Module"
        self.log = log
        self.run_contexts = run_contexts
        self.context = context
        self.request_object = request_object

    def get_name(self):
        return self.name

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
        options = {
            'request': self.onRequest,
            'status': self.onStatus,
            'response': self.onResponse,
        }
        if self.context in self.run_contexts:
            options[self.context](**keywords)
        else:
            self.log.msg("not my turn yet")

    def getProtocol(self):
        if self.context in ['request', 'response']:
            return self.request_object.clientproto
        else:
            raise Exception('Invalid context')

    def setProtocol(self, protocol):
        if self.context in ['request', 'response']:
            self.request_object.clientproto = protocol
        else:
            raise Exception('Invalid context')

    def getMethod(self):
        if self.context in ['request', 'response']:
            return self.request_object.method
        else:
            raise Exception('Invalid context')

    def setMethod(self, method):
        if self.context in ['request']:
            self.request_object.method = method
        else:
            raise Exception('Invalid context')

    def getURI(self):
        if self.context in ['request', 'response']:
            return self.request_object.uri
        else:
            raise Exception('Invalid context')

    def setURI(self, uri):
        if self.context in ['request']:
            self.request_object.uri = uri
        else:
            raise Exception('Invalid context')

    def getStatusCode(self):
        if self.context in ['response']:
            return self.request_object.code
        else:
            raise Exception('Invalid context')

    def setStatusCode(self, status_code):
        if self.context in ['response']:
            self.request_object.code = status_code
        else:
            raise Exception('Invalid context')

    def getStatusDescription(self):
        if self.context in ['response']:
            return self.request_object.code_message
        else:
            raise Exception('Invalid context')

    def setStatusDescription(self, status_description):
        if self.context in ['response']:
            self.request_object.code_message = status_description
        else:
            raise Exception('Invalid context')

    def getAllHeaders(self):
        if self.context == 'request':
            return self.request_object.requestHeaders.getAllRawHeaders()
        elif self.context == 'response':
            return self.request_object.responseHeaders.getAllRawHeaders()
        else:
            raise Exception('Invalid context')

    def hasHeader(self, name):
        if self.context == 'request':
            return self.request_object.requestHeaders.hasHeader(name)
        elif self.context == 'response':
            return self.request_object.responseHeaders.hasHeader(name)
        else:
            raise Exception('Invalid context')

    def getHeader(self, name):
        if self.context == 'request':
            return self.request_object.requestHeaders.getRawHeaders(name)
        elif self.context == 'response':
            return self.request_object.responseHeaders.getRawHeaders(name)
        else:
            raise Exception('Invalid context')

    def removeHeader(self, name):
        if self.context == 'request':
            return self.request_object.requestHeaders.removeHeader(name)
        elif self.context == 'response':
            return self.request_object.responseHeaders.removeHeader(name)
        else:
            raise Exception('Invalid context')

    def setHeader(self, name, value):
        if self.context == 'request':
            return self.request_object.requestHeaders.setRawHeaders(name,
                                                                    [value])
        elif self.context == 'response':
            return self.request_object.responseHeaders.setRawHeaders(name,
                                                                     [value])
        else:
            raise Exception('Invalid context')

    def getContent(self):
        if self.context in ['request', 'response']:
            if self.context == 'request':
                return self.request_object.content.getvalue()
            elif self.context == 'response':
                return self.request_object.response_content.getvalue()
        else:
            raise Exception('Invalid context')

    def setContent(self, content):
        if self.context in ['request', 'response']:
            self.setHeader('Content-Length', str(len(content)))
            self.request_object.content = io.BytesIO(content)
        else:
            raise Exception('Invalid context')

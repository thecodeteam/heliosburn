#!/usr/bin/env python
import sys
import subprocess
import os
from os.path import dirname, abspath, join
from inspect import getsourcefile
import yaml
import json
from twisted.internet import reactor
from twisted.web import http
from twisted.web import proxy
from twisted.web import server
from twisted.python import log
from twisted.web.proxy import ReverseProxy
from twisted.web.proxy import ReverseProxyRequest
from twisted.web.proxy import ReverseProxyResource
from twisted.web.proxy import ProxyClientFactory
from twisted.web.proxy import ProxyClient
from modules import *
"""
This is an example test

"""


# Set a marker for our code path
base_path = dirname(abspath(getsourcefile(lambda _: None)))

# Let's grab our config parameters
with open('./config.yaml', 'r+') as config_file:
    config = yaml.load(config_file.read())

# Set up logging
log_file = config['log']['path'].format(base_path)

try: 
    if config['log']['standard_out'].lower() == 'yes':
        setStdout = True
    else:
        setStdout = False
except KeyError:
    log.err()

#log.startLogging( open(log_file,'w'), setStdout = setStdout)
log.startLogging( open(log_file,'a') )

site = server.Site(proxy.ReverseProxyResource(config['upstream']['address'], 
                                                config['upstream']['port'],
                                                ''))
if 'http' in config['proxy']['protocols'] : 
    http_address = config['proxy']['bind']
    http_port = config['proxy']['protocols']['http']

upstream_host = config['upstream']['address']
upstream_port = config['upstream']['port']
request_object = None
response_object = None
log.msg(config)

def get_class(mod_dict):
    """
    Simple function which returns a class dynamically when passed a dictionary
    containing the appropriate information about a proxy module

    >>> with open('./config.yaml', 'r+') as config_file:
    ...     config = yaml.load(config_file.read())
    >>> run_modules(context = None)

    """
    log.msg("mod_dict: %s" % mod_dict)
    module_path = mod_dict['path']
    class_name = mod_dict['name']
    try:
        module = __import__(module_path, fromlist=[class_name])
    except ImportError:
        raise ValueError("Module '%s' could not be imported" % (module_path,))

    try:
        class_ = getattr(module, class_name)
    except AttributeError:
        raise ValueError("Module '%s' has no class '%s'" %(module_path, class_name,))
    return class_

def run_modules(context, request_object = None, response_object = None):
    """
    Runs all proxy modules in the order specified in config.yaml
    """
    for  module_dict in config['proxy']['modules']:
        class_ = get_class(module_dict)
        instance_ = class_( context=context,
                            request_object=request_object,
                            response_object=response_object,
                            run_contexts=module_dict['run_contexts'])
        instance_.run(**module_dict['kwargs'])

class MyProxyClient(ProxyClient):
    """
    ProxyClient extension used to customize handling of proxy responses.
    See Twisted's ProxyClient API documentation for details.


    >>> test_ProxyClient = MyProxyClient()

    """
 
    def handleStatus(self, version, code, message):
        """
        Invoked after a status code and message are received
        """
        # Here we can modify the status code
        # End of modifications
               
        ProxyClient.handleStatus(self, version, code, message)
 
    def handleHeader(self, key, value):
        """
        Invoked once for every Header received in a response
        """
        # Here we can modify the headers
        if key == "Server":
            value = "My custom server"
        # End of modifications
        
        ProxyClient.handleHeader(self, key, value)
               
    def handleResponseEnd(self):
        """
        Invoked at the end of every completed response
        """
        if self._finished:
            run_modules(context = 'response', response_object=self,
                        request_object=request_object)

        ProxyClient.handleResponseEnd(self)
               
 
class MyProxyClientFactory(ProxyClientFactory):
    """

    >>> test_ProyClientFactory = MyProxyClientFactory()
    """
    protocol = MyProxyClient
 
       

class MyReverseProxyRequest(ReverseProxyRequest):
    """
    ReverseProxyRequest extension used to customize handling of proxy requests.
    See Twisted's ReverseProxyRequest API documentation for details.

    >>> test_ReverseProxyRequest = MyReverseProxyRequest()

    """

    proxyClientFactoryClass = MyProxyClientFactory
       
    def process(self):
        """
        Implementation of Twisted's ReverseProxyReqeust.process() which
        processes request objects. Please see ReverseProxyRequest API
        documentation.
        """
        global request_object
        request_object = self

        run_modules(context = 'request',
                    request_object=self,
                    response_object=None)
        log.msg("VERB: {}.method, URI: {}.uri, HEADERS: {}.requestHeaders".format(self, self, self))
        
        self.requestHeaders.setRawHeaders(b"host", [upstream_host])
        clientFactory = self.proxyClientFactoryClass( self.method, self.uri,
                                                        self.clientproto,
                                                        self.getAllHeaders(),
                                                        self.content.read(),
                                                        self)
        self.reactor.connectTCP(upstream_host, upstream_port, clientFactory)
       
 
class MyReverseProxyResource(ReverseProxyResource):
    """
    ReverseProxyResource extension used to customize handling of proxy
    requests.  See Twisted's ReverseProxyResource API documentation for
    details.

    >>> test_ReverseProxyResource = MyReverseProxyResource()

    """
    proxyClientFactoryClass = MyProxyClientFactory
       
    def getChild(self, path, request):
        """
        return host, port, URI, and reactor instance

        >>> getchile(self, '/', MyReverseProxyRequest())

        """
        return MyReverseProxyResource(
                                        self.host, self.port,
                                        self.path + '/' + urlquote(path, safe=""),
                                        self.reactor)
 
               
def run_proxy():
    """
    Entry point for starting the proxy
    """
    run_modules(context='None')
    resource = MyReverseProxyResource(upstream_host, upstream_port, '')              
    f = server.Site(resource)
    f.requestFactory = MyReverseProxyRequest
    reactor.listenTCP(http_port, f, interface=http_address)
    reactor.run()

def test_check():
    if 'test' in sys.argv:
        return True

def prep_background():
    """
    Launch background servers for assistance in testing

    >>> length(prep_background())
    2
    """
    try:
        ts_pid = os.spawnl(os.P_NOWAIT,['./tests/testserver.py'])
        redis_pid = os.spawnl(os.P_NOWAIT,['/usr/local/redis/src/redis-server'])
    except:
        log.error()
    return (ts_pid, redis_pid)

def run_tests():
    import doctest
    doctest.testmod()

try: 
    prep_background()
except:
    log.error()

if __name__ == "__main__":
    run_proxy
    if test_check():
        run_tests()
    else:
        run_proxy()

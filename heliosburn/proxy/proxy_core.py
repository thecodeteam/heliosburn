import sys
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
from modules import addLag



print dir()
print globals()
with open('./config.yaml', 'r+') as config_file:
    config = yaml.load(config_file.read())

log.startLogging(sys.stdout)

site = server.Site(proxy.ReverseProxyResource(config['upstream']['address'], 
                                                config['upstream']['port'],
                                                ''))
if 'http' in config['proxy']['protocols'] : 
    http_address = config['proxy']['bind']
    http_port = config['proxy']['protocols']['http']

upstream_host = config['upstream']['address']
upstream_port = config['upstream']['port']

 
print config

def get_class(mod_dict):
    print "mod_dict: %s" % mod_dict
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

class MyProxyClient(ProxyClient):
 
        def handleStatus(self, version, code, message):
                # Here we can modify the status code
                #code = 404
                #code = 220
                #message = "Not found"
                # End of modifications
                print "UPSTREAM CODE:"
                print code
               
                ProxyClient.handleStatus(self, version, code, message)
 
        def handleHeader(self, key, value):
                # Here we can modify the headers
                if key == "Server":
                        value = "My custom server"
                # End of modifications
               
                ProxyClient.handleHeader(self, key, value)
               
        def handleResponseEnd(self):
                if self._finished:
                    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                    print "UPSTREAM CODE :  %s" % (self.father.code)
                    print "UPSTREAM MSG :  %s" % (self.father.code_message)
                    print "UPSTREAM HEADERS : %s" % (self.father.responseHeaders)
                    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"

                    for  module_dict in config['proxy']['modules']:
                        class_ = get_class(module_dict)
                        print class_
                        print type(class_)
                        instance_ = class_( context='response', proxy_object=self,
                                        run_contexts=module_dict['run_contexts'])
                        instance_.run(**module_dict['kwargs'])

                ProxyClient.handleResponseEnd(self)
               
 
class MyProxyClientFactory(ProxyClientFactory):
        protocol = MyProxyClient
 
       

class MyReverseProxyRequest(ReverseProxyRequest):
        proxyClientFactoryClass = MyProxyClientFactory
       
        def process(self):
               
                for  module_dict in config['proxy']['modules']:
                    class_ = get_class(module_dict)
                    print class_
                    print type(class_)
                    instance_ = class_( context='request', proxy_object=self,
                                        run_contexts=module_dict['run_contexts'])
                    instance_.run(**module_dict['kwargs'])

                print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                print "VERB : %s" % (self.method)
                print "URI : %s" % (self.uri)
                print "HEADERS : %s" % (self.requestHeaders)
                print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

               
                self.requestHeaders.setRawHeaders(b"host", [upstream_host])
                clientFactory = self.proxyClientFactoryClass(
                self.method, self.uri, self.clientproto, self.getAllHeaders(),
                self.content.read(), self)
                self.reactor.connectTCP(upstream_host, upstream_port, clientFactory)
       
 
class MyReverseProxyResource(ReverseProxyResource):
 
        proxyClientFactoryClass = MyProxyClientFactory
       
        def getChild(self, path, request):
                return MyReverseProxyResource(
                        self.host, self.port, self.path + '/' + urlquote(path, safe=""),
                        self.reactor)
 
               
resource = MyReverseProxyResource(upstream_host, upstream_port, '')              
f = server.Site(resource)
f.requestFactory = MyReverseProxyRequest
reactor.listenTCP(http_port, f, interface=http_address)
reactor.run()

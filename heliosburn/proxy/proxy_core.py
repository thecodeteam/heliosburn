import sys
import yaml
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


with open('./config.yaml', 'r+') as config_file:
    params = yaml.load(config_file.read())

log.startLogging(sys.stdout)

site = server.Site(proxy.ReverseProxyResource(params['upstream']['address'], 
                                                params['upstream']['port'],
                                                ''))
if 'http' in params['proxy']['protocols'] : 
    http_address = params['proxy']['protocols']
    http_port = 8880

upstream_host = params['upstream']['address']
upstream_port = params['upstream']['port']
 
class MyProxyClient(ProxyClient):
 
        def handleStatus(self, version, code, message):
                # Here we can modify the status code
                #code = 404
                #code = 220
                #message = "Not found"
                # End of modifications
                print "UPSTREAM CODE:"
                print code
                #print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                #print "UPSTREAM CODE :  %s" % (self.father.code)
                #print "UPSTREAM MSG :  %s" % (self.father.code_message)
                #print "UPSTREAM HEADERS : %s" % (self.father.responseHeaders)
                #print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
               
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
                       
                ProxyClient.handleResponseEnd(self)
               
 
class MyProxyClientFactory(ProxyClientFactory):
        protocol = MyProxyClient
 
       
class MyReverseProxyRequest(ReverseProxyRequest):
        proxyClientFactoryClass = MyProxyClientFactory
       
        def process(self):
               
                # Here we can add modifications to the Request:
                #self.method = 'POST'
                # End of modifications
               
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
reactor.listenTCP(http_port, f)
reactor.run()

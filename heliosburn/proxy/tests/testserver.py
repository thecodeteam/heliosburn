# Simple server that receives any traffic and responds with the URL and querystring arguments
# This is intended to be used for unit tests and verifying the proxy functionality
import cherrypy
import pprint


class DummyReceiver(object):

    def default(self, *pargs, **kwargs):
        pp = pprint.PrettyPrinter()

        headers = pp.pformat(cherrypy.request.headers)
        return """pargs: '%s'\nkwargs: '%s'\nheaders:\n%s\n""" % (pargs, kwargs, headers)
    default.exposed = True

    def status404(self, *pargs, **kwargs):
        raise cherrypy.NotFound()
    status404.exposed = True

cherrypy.config.update({'server.socket_port': 8080})
cherrypy.quickstart(DummyReceiver(), '/')
# Simple server that receives any traffic and responds with the URL and querystring arguments
# This is intended to be used for unit tests and verifying the proxy functionality
import cherrypy


class DummyReceiver(object):

    def default(*pargs, **kwargs):
        return "pargs '%s' kwargs '%s'\n" % (pargs, kwargs)
    default.exposed = True

cherrypy.config.update({'server.socket_port': 8080})
cherrypy.quickstart(DummyReceiver(), '/')
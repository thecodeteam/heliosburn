# Simple server that receives any traffic and responds with the URL and querystring arguments
# This is intended to be used for unit tests and verifying the proxy functionality
import cherrypy
import pprint
import logging


class DummyReceiver(object):

    def default(self, *pargs, **kwargs):
        """
        Returns the URL as list, querystring args as dict, and headers as dict.
        """
        pp = pprint.PrettyPrinter()
        headers = pp.pformat(cherrypy.request.headers)
        cherrypy.log(headers)
        return """pargs: '%s'\nkwargs: '%s'\nheaders:\n%s\n""" % (pargs, kwargs, headers)
    default.exposed = True

    def fail(self, failure_type):
        """
        Returns some generic non-200 responses, based on failure_type.
        """
        if failure_type == "404":
            raise cherrypy.NotFound()
        elif failure_type == "403":
            raise cherrypy.HTTPError(403)
        else:
            raise cherrypy.HTTPError()
    fail.exposed = True

    def die(self):
        """
        Causes CherryPy's engine to exit cleanly.
        """
        cherrypy.log("DIE received")
        cherrypy.engine.exit()
    die.exposed = True


def main():
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.quickstart(DummyReceiver(), '/')

if __name__ == "__main__":
    main()
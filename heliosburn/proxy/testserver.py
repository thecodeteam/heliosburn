# Simple server that receives any traffic and responds with the URL and querystring arguments
# This is intended to be used for unit tests and verifying the proxy functionality
import cherrypy
import pprint


class DummyReceiver(object):

    def default(self, *pargs, **kwargs):
        """
        Return a serialized reprensentation of the URL, headers, querystring arguments, and body

        INFO: The default() function in CherryPy receives all non-matching URL's, so this function
        will be called for any URL except "/fail" and "/die"
        """
        import cherrypy
        pp = pprint.PrettyPrinter()
        headers = pp.pformat(cherrypy.request.headers)
        cherrypy.log(headers)
        body = cherrypy.request.body.fp.read()
        return """pargs: '%s'\nkwargs: '%s'\nheaders:\n%s\nbody:\n%s\n""" % (pargs, kwargs, headers, body)
    default.exposed = True

    def fail(self, failure_type):
        """
        Return some generic non-200 responses, based on failure_type.
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
        Cause CherryPy's engine to exit cleanly.

        NOTE: This is used by the unit tests to communicate to CherryPy's thread that it should shut down.
        """
        cherrypy.log("DIE received")
        cherrypy.engine.exit()
    die.exposed = True


def main():
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.quickstart(DummyReceiver(), '/')

if __name__ == "__main__":
    main()
import os
import cherrypy
from cherrypy import wsgiserver
from cherrypy.wsgiserver import ssl_builtin
from hbproject import wsgi as django_wsgi

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class Root(object):
    pass


def make_static_config(static_dir_name):
    """
    All custom static configurations are set here, since most are common, it
    makes sense to generate them just once.
    """
    static_path = os.path.join('/', static_dir_name)
    path = os.path.join(PATH, static_dir_name)
    configuration = {static_path: {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': path}
    }
    print configuration
    return cherrypy.tree.mount(Root(), '/', config=configuration)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000

    application = wsgiserver.WSGIPathInfoDispatcher({
        '/': django_wsgi.application,
        '/static': make_static_config('static')})

    server = wsgiserver.CherryPyWSGIServer(
        (host, port), application,
        server_name=None, numthreads=2, timeout=30, max=500)
    print("WSGI-hosting Server started on %s:%s" % (host, port))
    server.start()


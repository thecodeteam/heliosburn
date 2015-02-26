import os
import cherrypy
from cherrypy import wsgiserver

import dotenv
dotenv.read_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT')

if ENVIRONMENT == 'STAGING':
    settings = 'staging'
elif ENVIRONMENT == 'PRODUCTION':
    settings = 'production'
else:
    settings = 'development'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hbproject.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', settings.title())

from configurations import importer
importer.install()

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
        server_name=None, numthreads=10, timeout=5, max=100)
    print("WSGI-hosting Server started on %s:%s" % (host, port))
    try:
        server.start()
    except KeyboardInterrupt:
        cherrypy.engine.exit()
        print("Trapped exit, shutting down...")
        os._exit(1)


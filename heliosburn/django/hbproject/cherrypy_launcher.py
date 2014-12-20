from cherrypy import wsgiserver
from cherrypy.wsgiserver import ssl_builtin
from hbproject import wsgi as django_wsgi

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    server = wsgiserver.CherryPyWSGIServer(
        (host, port), django_wsgi.application,
        server_name=None, numthreads=2, timeout=30, max=500)
    print("WSGI-hosting Server started on %s:%s" % (host, port))
    server.start()


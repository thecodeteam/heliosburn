import unittest
from threading import Thread
import time
import testserver
import urllib2
import logging


class TestServer(Thread):
    def run(self):
        testserver.main()


class ProxyCoreTest(unittest.TestCase):

    def setUp(self):
        logging.warning("Spawning TestServer in a thread")
        self.testserver_thread = TestServer()
        self.testserver_thread.start()
        time.sleep(1)  # Let cherrypy engine thread start and begin listening

        logging.warning("Starting proxy_core")

    def tearDown(self):
        logging.warning("Shutting down TestServer gracefully")
        time.sleep(1)  # Let cherrypy engine be idle before sending /die
        urllib2.urlopen("http://127.0.0.1:8080/die")
        time.sleep(1)  # Let cherrypy thread exit cleanly
        assert self.testserver_thread.is_alive() is False

    def test_proxy_logs_200(self):
        logging.warning("Testing logging of HTTP 200")
        x = urllib2.urlopen("http://127.0.0.1:8080")
        pass
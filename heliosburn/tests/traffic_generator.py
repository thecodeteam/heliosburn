#!/usr/bin/python
import requests
import signal
import time
import random
import os
import sys


PROXY_HOST = 'localhost'
PROXY_PORT = 8880
SLEEP_MIN = 0.1
SLEEP_MAX = 0.2
PATHS = [
    '/static/webui/css/heliosburn.css',
    '/static/webui/img/avatar5.png',
    '/static/webui/js/AdminLTE/app.js',
    '/static/webui/css/datatables/dataTables.bootstrap.css',
    '/static/webui/css/AdminLTE.css',
    '/static/webui/css/images/sort_both.png',
    '/static/webui/js/plugins/flot/jquery.flot.resize.min.js'
]


def main():
    count = 0

    while True:
        url = 'http://%s:%d%s' % (PROXY_HOST, PROXY_PORT, random.choice(PATHS))
        requests.get(url)
        print '* Request sent (%d)' % (count,)
        time.sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))
        count += 1


def signal_handler(signal, frame):
    print '\nExiting...'
    os.system("stty echo")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()

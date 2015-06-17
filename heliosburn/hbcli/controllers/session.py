import argparse
import sys
import os
import re
import json
from IPython.core.debugger import Tracer


def main(config, args):
    description = "Interact with session objects."
    m = re.match(r'^.*\.(.*)$', __name__)
    controller_name = m.groups()[0]
    del sys.argv[1]
    parser = argparse.ArgumentParser(prog="%s %s" % (sys.argv[0], controller_name), description=description)
    parser.add_argument("action", type=str, choices=("create", "read", "update", "delete"), help="action to perform with session object")
    args = vars(parser.parse_args())

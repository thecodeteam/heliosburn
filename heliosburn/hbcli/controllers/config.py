import argparse
import sys
import os
import re
import json
from IPython.core.debugger import Tracer


def main(config, args):
    description = "Updates the API configuration values in $HOME/.hbclirc"
    m = re.match(r'^.*\.(.*)$', __name__)
    controller_name = m.groups()[0]
    del sys.argv[1]
    parser = argparse.ArgumentParser(prog="%s %s" % (sys.argv[0], controller_name), description=description)
    parser.add_argument("url", type=str, help="URL to Helios Burn API")
    parser.add_argument("user", type=str, help="Username for Helios Burn API")
    parser.add_argument("pass", type=str, help="Password for Helios Burn API")
    args = vars(parser.parse_args())
    try:
        path = os.environ['HOME'] + "/.hbclirc"
        f = open(path, "w")
        f.write(json.dumps(args))
        f.close()
        print("Saved configuration to %s" % path)
    except Exception as e:
        print("Error saving config: %s" % e)
        sys.exit(1)

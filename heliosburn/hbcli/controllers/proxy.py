import argparse
import sys
import re
import json
import requests
from models import auth
import pdb
import pprint


def status(config, args):
    pp = pprint.PrettyPrinter()
    url = config['url'] + "/api/proxy/status/"

    token = auth.get_token(config)
    r = requests.get(url, headers={"X-Auth-Token": token})
    if r.status_code != 200:
        print("API returned status code %s" % (r.status_code))
        sys.exit(1)
    else:
        pp.pprint(json.loads(r.content))


def main(config, args):
    description = "Interact with the proxy."
    m = re.match(r'^.*\.(.*)$', __name__)
    controller_name = m.groups()[0]
    del sys.argv[1]
    parser = argparse.ArgumentParser(prog="%s %s" % (sys.argv[0], controller_name), description=description)
    subparsers = parser.add_subparsers(dest="action")

    # status
    read_parser = subparsers.add_parser("status", help="read proxy status")

    args = vars(parser.parse_args())
    action_map = {
        "status": status,
    }
    action_map[args['action']](config, args)

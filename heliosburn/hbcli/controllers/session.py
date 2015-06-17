import argparse
import sys
import re
import json
import requests
from models import auth
import pdb
import pprint


def create(config, args):
    pass


def read(config, args):
    pp = pprint.PrettyPrinter()
    url = config['url'] + "/api/session/"
    if (args['all'] is False) and (args['session'] is None):
        print("No session(s) specified to read.")
        return
    elif args['all'] is True:
        token = auth.get_token(config)
        r = requests.get(url, headers={"X-Auth-Token": token})
        if r.status_code != 200:
            print("API returned status code %s" % (r.status_code))
            sys.exit(1)
        else:
            pp.pprint(json.loads(r.content))
    elif args['session'] is not None:
        url += args['session'] + "/"
        token = auth.get_token(config)
        r = requests.get(url, headers={"X-Auth-Token": token})
        pass


def update(config, args):
    pass


def delete(config, args):
    pass


def main(config, args):
    description = "Interact with session objects."
    m = re.match(r'^.*\.(.*)$', __name__)
    controller_name = m.groups()[0]
    del sys.argv[1]
    parser = argparse.ArgumentParser(prog="%s %s" % (sys.argv[0], controller_name), description=description)
    subparsers = parser.add_subparsers(dest="action")
    
    # create 
    create_parser = subparsers.add_parser("create", help="create session object")
    create_parser.add_argument("--stub", type=str, required=True, help="stub desc")

    # read
    read_parser = subparsers.add_parser("read", help="read session object(s)")
    read_parser.add_argument("--stub", type=str, required=True, help="stub desc")
    
    # update 
    update_parser = subparsers.add_parser("update", help="update existing session object")
    update_parser.add_argument("--stub", type=str, required=True, help="stub desc")

    # delete
    delete_parser = subparsers.add_parser("delete", help="delete session object")
    delete_parser.add_argument("--stub", type=str, required=True, help="stub desc")
    
    args = vars(parser.parse_args())
    action_map = {
        "create": create,
        "read": read,
        "update": update,
        "delete": delete,
    }
    action_map[args['action']](config, args)

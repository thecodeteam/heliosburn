import argparse
import sys
import re
import json
import requests
from models import auth
import pdb
import pprint


def create(config, args):
    pp = pprint.PrettyPrinter()
    url = config['url'] + "/api/session/"

    data = {
       "name": args['name'],
       "description": args['description'],
       "upstreamHost": args['upstreamHost'],
       "upstreamPort": args['upstreamPort'],
    }

    if args['testplan'] is not None:
        data['testplan'] = args['testplan']

    if args['serverOverloadProfile'] is not None:
        data['serverOverloadProfile'] = {"id": args['serverOverloadProfile']}

    if args['qosProfile'] is not None:
        data['qosProfile'] = {"id": args['qosProfile']}

    pdb.set_trace()

    token = auth.get_token(config)
    r = requests.post(url, data=json.dumps(data), headers={"X-Auth-Token": token})
    if r.status_code != 200:
        print("API returned status code %s" % (r.status_code))
        sys.exit(1)
    else:
        pp.pprint(json.loads(r.content))

def read(config, args):
    pp = pprint.PrettyPrinter()
    url = config['url'] + "/api/session/"

    if (args['all'] is False) and (args['session'] is None):
        print("No session(s) specified to read. Use -h to see usage.")
        return
    elif args['session'] is not None:
        url += args['session'] + "/"

    token = auth.get_token(config)
    r = requests.get(url, headers={"X-Auth-Token": token})
    if r.status_code != 200:
        print("API returned status code %s" % (r.status_code))
        sys.exit(1)
    else:
        pp.pprint(json.loads(r.content))


def update(config, args):
    pass


def delete(config, args):
    pass

def start(config, args):
    pass

def stop(config, args):
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
    create_parser.add_argument("--name", type=str, required=True, help="session name")
    create_parser.add_argument("--description", type=str, required=True, help="session description")
    create_parser.add_argument("--upstreamHost", type=str, required=True, help="upstream hostname")
    create_parser.add_argument("--upstreamPort", type=int, required=True, help="upstream port number")
    create_parser.add_argument("--testplan", type=str, help="testplan id")
    create_parser.add_argument("--serverOverloadProfile", type=str, help="server overload profile id")
    create_parser.add_argument("--qosProfile", type=str, help="qos profile id")
    

    # read
    read_parser = subparsers.add_parser("read", help="read session object(s)")
    read_parser.add_argument("--all", action="store_const", const=True, default=False, help="read all sessions")
    read_parser.add_argument("--session", type=str, help="ID of session to read")
    
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

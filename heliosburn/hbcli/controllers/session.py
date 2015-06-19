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
    url = config['url'] + "/api/session/" + args['session'] + "/"

    data = {}

    if args['name'] is not None:
        data['name'] = args['name']

    if args['description'] is not None:
        data['description'] = args['description']

    if args['upstreamHost'] is not None:
        data['upstreamHost'] = args['upstreamHost']

    if args['upstreamPort'] is not None:
        data['upstreamPort'] = args['upstreamPort']

    if args['testplan'] is not None:
        data['testplan'] = args['testplan']

    if args['serverOverloadProfile'] is not None:
        data['serverOverloadProfile'] = {"id": args['serverOverloadProfile']}

    if args['qosProfile'] is not None:
        data['qosProfile'] = {"id": args['qosProfile']}

    token = auth.get_token(config)
    r = requests.put(url, data=json.dumps(data), headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def delete(config, args):
    url = config['url'] + "/api/session/" + args['session'] + "/"
    token = auth.get_token(config)
    r = requests.delete(url, headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def start(config, args):
    url = config['url'] + "/api/session/" + args['session'] + "/start/"
    token = auth.get_token(config)
    r = requests.get(url, headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def stop(config, args):
    url = config['url'] + "/api/session/" + args['session'] + "/start/"
    token = auth.get_token(config)
    r = requests.get(url, headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def main(config, args):
    description = "Interact with session objects."
    m = re.match(r'^.*\.(.*)$', __name__)
    controller_name = m.groups()[0]
    del sys.argv[1]
    parser = argparse.ArgumentParser(prog="%s %s" % (sys.argv[0], controller_name), description=description)
    subparsers = parser.add_subparsers(dest="action")

    # create
    create_parser = subparsers.add_parser("create", help="create session object")
    create_parser_required = create_parser.add_argument_group("required arguments")
    create_parser_required.add_argument("--name", type=str, required=True, help="session name")
    create_parser_required.add_argument("--description", type=str, required=True, help="session description")
    create_parser_required.add_argument("--upstreamHost", type=str, required=True, help="upstream hostname")
    create_parser_required.add_argument("--upstreamPort", type=int, required=True, help="upstream port number")
    create_parser.add_argument("--testplan", type=str, help="testplan id")
    create_parser.add_argument("--serverOverloadProfile", type=str, help="server overload profile id")
    create_parser.add_argument("--qosProfile", type=str, help="qos profile id")

    # read
    read_parser = subparsers.add_parser("read", help="read session object(s)")
    read_parser.add_argument("--all", action="store_const", const=True, default=False, help="read all sessions")
    read_parser.add_argument("--session", type=str, help="ID of session to read")

    # update
    update_parser = subparsers.add_parser("update", help="update existing session object")
    update_parser_required = update_parser.add_argument_group("required arguments")
    update_parser_required.add_argument("--session", type=str, required=True, help="session id to update")
    update_parser.add_argument("--name", type=str, help="session name")
    update_parser.add_argument("--description", type=str, help="session description")
    update_parser.add_argument("--upstreamHost", type=str, help="upstream hostname")
    update_parser.add_argument("--upstreamPort", type=int, help="upstream port number")
    update_parser.add_argument("--testplan", type=str, help="testplan id")
    update_parser.add_argument("--serverOverloadProfile", type=str, help="server overload profile id")
    update_parser.add_argument("--qosProfile", type=str, help="qos profile id")

    # delete
    delete_parser = subparsers.add_parser("delete", help="delete session object")
    delete_parser_required = delete_parser.add_argument_group("required arguments")
    delete_parser_required.add_argument("--session", type=str, required=True, help="session id to delete")

    # start 
    start_parser = subparsers.add_parser("start", help="start a running session")
    start_parser_required = start_parser.add_argument_group("required arguments")
    start_parser_required.add_argument("--session", type=str, required=True, help="session id to start")

    # stop 
    stop_parser = subparsers.add_parser("stop", help="stop a running session")
    stop_parser_required = stop_parser.add_argument_group("required arguments")
    stop_parser_required.add_argument("--session", type=str, required=True, help="session id to stop")


    args = vars(parser.parse_args())
    action_map = {
        "create": create,
        "read": read,
        "update": update,
        "delete": delete,
        "start": start,
        "stop": stop,
    }
    action_map[args['action']](config, args)

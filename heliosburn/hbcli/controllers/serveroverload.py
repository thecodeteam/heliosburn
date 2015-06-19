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
    url = config['url'] + "/api/serveroverload/"

    data = {
       "name": args['name'],
       "description": args['description'],
       "function": { 
            "type": args['functiontype'],
            "expValue": args['functionexpvalue'],
            "growthRate": args['functiongrowthrate'],
       },
    }

    # TODO: response triggers

    token = auth.get_token(config)
    r = requests.post(url, data=json.dumps(data), headers={"X-Auth-Token": token})
    if r.status_code != 200:
        print("API returned status code %s" % (r.status_code))
        sys.exit(1)
    else:
        pp.pprint(json.loads(r.content))


def read(config, args):
    pp = pprint.PrettyPrinter()
    url = config['url'] + "/api/serveroverload/"

    if (args['all'] is False) and (args['serveroverloadprofile'] is None):
        print("No serveroverload(s) specified to read. Use -h to see usage.")
        return
    elif args['serveroverloadprofile'] is not None:
        url += args['serveroverloadprofile'] + "/"

    token = auth.get_token(config)
    r = requests.get(url, headers={"X-Auth-Token": token})
    if r.status_code != 200:
        print("API returned status code %s" % (r.status_code))
        sys.exit(1)
    else:
        pp.pprint(json.loads(r.content))


def update(config, args):
    url = config['url'] + "/api/serveroverload/" + args['serveroverload'] + "/"

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
    url = config['url'] + "/api/serveroverload/" + args['serveroverload'] + "/"
    token = auth.get_token(config)
    r = requests.delete(url, headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def main(config, args):
    description = "Interact with serveroverload profile objects."
    m = re.match(r'^.*\.(.*)$', __name__)
    controller_name = m.groups()[0]
    del sys.argv[1]
    parser = argparse.ArgumentParser(prog="%s %s" % (sys.argv[0], controller_name), description=description)
    subparsers = parser.add_subparsers(dest="action")

    # create
    create_parser = subparsers.add_parser("create", help="create serveroverload profile object")
    create_parser_required = create_parser.add_argument_group("required arguments")
    create_parser_required.add_argument("--name", type=str, required=True, help="serveroverload name")
    create_parser_required.add_argument("--description", type=str, required=True, help="serveroverload description")
    create_parser_required.add_argument("--functiontype", type=str, required=True, help="function type")
    create_parser_required.add_argument("--functionexpvalue", type=str, required=True, help="function exp value")
    create_parser_required.add_argument("--functiongrowthrate", type=str, required=True, help="function growth rate")
    create_parser_required.add_argument("--responsetrigger", type=str, required=True, help="response trigger") 
    # TODO 

    # read
    read_parser = subparsers.add_parser("read", help="read serveroverload profile object(s)")
    read_parser.add_argument("--all", action="store_const", const=True, default=False, help="read all serveroverload profiles")
    read_parser.add_argument("--serveroverloadprofile", type=str, help="ID of serveroverload profile to read")

    # update
    update_parser = subparsers.add_parser("update", help="update existing serveroverload profile object")
    update_parser_required = update_parser.add_argument_group("required arguments")
    update_parser_required.add_argument("--serveroverload", type=str, required=True, help="serveroverload profile id to update")

    # delete
    delete_parser = subparsers.add_parser("delete", help="delete serveroverload profile object")
    delete_parser_required = delete_parser.add_argument_group("required arguments")
    delete_parser_required.add_argument("--serveroverload", type=str, required=True, help="serveroverload profile id to delete")

    args = vars(parser.parse_args())
    action_map = {
        "create": create,
        "read": read,
        "update": update,
        "delete": delete,
    }
    action_map[args['action']](config, args)

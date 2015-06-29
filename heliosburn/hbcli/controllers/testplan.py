import argparse
import sys
import re
import json
import requests
from models import auth
import pprint


def create(config, args):
    pp = pprint.PrettyPrinter()
    url = config['url'] + "/api/testplan/"

    data = {
       "name": args['name'],
        "description": args['description'],
    }

    token = auth.get_token(config)
    r = requests.post(url, data=json.dumps(data), headers={"X-Auth-Token": token})
    if r.status_code != 200:
        print("API returned status code %s" % (r.status_code))
        sys.exit(1)
    else:
        pp.pprint(json.loads(r.content))


def read(config, args):
    pp = pprint.PrettyPrinter()
    url = config['url'] + "/api/testplan/"

    if (args['all'] is False) and (args['testplan'] is None):
        print("No testplan(s) specified to read. Use -h to see usage.")
        return
    elif args['testplan'] is not None:
        url += args['testplan'] + "/"

    token = auth.get_token(config)
    r = requests.get(url, headers={"X-Auth-Token": token})
    if r.status_code != 200:
        print("API returned status code %s" % (r.status_code))
        sys.exit(1)
    else:
        testplans = json.loads(r.content)
        pp.pprint(testplans)


def update(config, args):
    url = config['url'] + "/api/testplan/" + args['testplan'] + "/"

    data = {}

    if args['name'] is not None:
        data['name'] = args['name']

    if args['description'] is not None:
        data['description'] = args['description']

    token = auth.get_token(config)
    r = requests.put(url, data=json.dumps(data), headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def delete(config, args):
    url = config['url'] + "/api/testplan/" + args['testplan'] + "/"
    token = auth.get_token(config)
    r = requests.delete(url, headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def main(config, args):
    description = "Interact with testplan objects."
    m = re.match(r'^.*\.(.*)$', __name__)
    controller_name = m.groups()[0]
    del sys.argv[1]
    parser = argparse.ArgumentParser(prog="%s %s" % (sys.argv[0], controller_name), description=description)
    subparsers = parser.add_subparsers(dest="action")

    # create
    create_parser = subparsers.add_parser("create", help="create testplan object")
    create_parser_required = create_parser.add_argument_group("required arguments")
    create_parser_required.add_argument("--name", type=str, required=True)
    create_parser.add_argument("--description", type=str)

    # read
    read_parser = subparsers.add_parser("read", help="read testplan object(s)")
    read_parser.add_argument("--all", action="store_const", const=True, default=False, help="read all testplans")
    read_parser.add_argument("--testplan", type=str, help="ID of testplan to read")

    # update
    update_parser = subparsers.add_parser("update", help="update existing testplan object")
    update_parser_required = update_parser.add_argument_group("required arguments")
    update_parser_required.add_argument("--testplan", type=str, required=True, help="testplan id to update")
    update_parser.add_argument("--name", type=str)
    update_parser.add_argument("--description", type=str)

    # delete
    delete_parser = subparsers.add_parser("delete", help="delete testplan object")
    delete_parser_required = delete_parser.add_argument_group("required arguments")
    delete_parser_required.add_argument("--testplan", type=str, required=True, help="testplan id to delete")

    args = vars(parser.parse_args())
    action_map = {
        "create": create,
        "read": read,
        "update": update,
        "delete": delete,
    }
    action_map[args['action']](config, args)

import argparse
import sys
import re
import json
import requests
from models import auth
import pprint
import pdb


def create(config, args):
    pp = pprint.PrettyPrinter()
    url = config['url'] + "/api/testplan/" + args['testplan'] + "/rule/"

    token = auth.get_token(config)
    r = requests.post(url, data=args['rulejson'], headers={"X-Auth-Token": token})
    if r.status_code != 200:
        print("API returned status code %s" % (r.status_code))
        sys.exit(1)
    else:
        pp.pprint(json.loads(r.content))


def update(config, args):
    url = config['url'] + "/api/testplan/" + args['testplan'] + "/rule/" + args['rule'] + "/"
    token = auth.get_token(config)
    r = requests.put(url, data=args['rulejson'], headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def delete(config, args):
    url = config['url'] + "/api/testplan/" + args['testplan'] + "/rule/" + args['rule'] + "/"
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
    create_parser = subparsers.add_parser("create", help="create rule within testplan object")
    create_parser_required = create_parser.add_argument_group("required arguments")
    create_parser_required.add_argument("--testplan", type=str, required=True)
    create_parser_required.add_argument("--rulejson", type=str, required=True, help="JSON representation of rule")

    # update
    update_parser = subparsers.add_parser("update", help="update rule within testplan object")
    update_parser_required = update_parser.add_argument_group("required arguments")
    update_parser_required.add_argument("--testplan", type=str, required=True)
    update_parser_required.add_argument("--rule", type=str, required=True, help="rule id to update")
    update_parser_required.add_argument("--rulejson", type=str, required=True, help="JSON representation of rule")

    # delete
    delete_parser = subparsers.add_parser("delete", help="delete rule within testplan object")
    delete_parser_required = delete_parser.add_argument_group("required arguments")
    delete_parser_required.add_argument("--testplan", type=str, required=True, help="testplan id")
    delete_parser_required.add_argument("--rule", type=str, required=True, help="testplan id to delete")

    args = vars(parser.parse_args())
    action_map = {
        "create": create,
        "delete": delete,
        "update": update,
    }
    action_map[args['action']](config, args)

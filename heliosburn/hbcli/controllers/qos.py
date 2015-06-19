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
    url = config['url'] + "/api/qos/"

    data = {
       "name": args['name'],
       "description": args['description'],
       "latency": args['latency'],
       "jitter": {
            "min": args['jittermin'],
            "max": args['jittermax'],
       },
       "trafficLoss": args['trafficloss'],
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
    url = config['url'] + "/api/qos/"

    if (args['all'] is False) and (args['qosprofile'] is None):
        print("No qos profile(s) specified to read. Use -h to see usage.")
        return
    elif (args['qosprofile'] is not None) and (args['all'] is False):
        url += args['qosprofile'] + "/"

    token = auth.get_token(config)
    r = requests.get(url, headers={"X-Auth-Token": token})
    if r.status_code != 200:
        print("API returned status code %s" % (r.status_code))
        sys.exit(1)
    else:
        pp.pprint(json.loads(r.content))


def update(config, args):
    url = config['url'] + "/api/qos/" + args['qosprofile'] + "/"

    data = {}

    if args['name'] is not None:
        data['name'] = args['name']

    if args['latency'] is not None:
        data['latency'] = args['latency']

    if args['description'] is not None:
        data['description'] = args['description']

    if (args['jittermin'] is not None) or (args['jittermax'] is not None):
        data['jitter'] = {
            "min": args['jittermin'],
            "max": args['jittermax'],
        }

    if args['trafficloss'] is not None:
        data['trafficLoss'] = args['trafficloss']

    token = auth.get_token(config)
    r = requests.put(url, data=json.dumps(data), headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def delete(config, args):
    url = config['url'] + "/api/qos/" + args['qosprofile'] + "/"
    token = auth.get_token(config)
    r = requests.delete(url, headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def main(config, args):
    description = "Interact with qos objects."
    m = re.match(r'^.*\.(.*)$', __name__)
    controller_name = m.groups()[0]
    del sys.argv[1]
    parser = argparse.ArgumentParser(prog="%s %s" % (sys.argv[0], controller_name), description=description)
    subparsers = parser.add_subparsers(dest="action")

    # create
    create_parser = subparsers.add_parser("create", help="create qos profile object")
    create_parser_required = create_parser.add_argument_group("required arguments")
    create_parser_required.add_argument("--name", type=str, required=True, help="qos profile name")
    create_parser.add_argument("--latency", type=float, help="qos profile latency")
    create_parser.add_argument("--jittermin", type=float, help="qos profile minimum jitter")
    create_parser.add_argument("--jittermax", type=float, help="qos profile maximum jitter")
    create_parser.add_argument("--trafficloss", type=float, help="qos profile traffic loss")
    create_parser.add_argument("--description", type=str, help="qos profile description")

    # read
    read_parser = subparsers.add_parser("read", help="read qos profile object(s)")
    read_parser.add_argument("--all", action="store_const", const=True, default=False, help="read all qos profiles")
    read_parser.add_argument("--qosprofile", type=str, help="qos profile id to read")

    # update
    update_parser = subparsers.add_parser("update", help="update existing qos profile object")
    update_parser_required = update_parser.add_argument_group("required arguments")
    update_parser_required.add_argument("--qosprofile", type=str, required=True, help="qos profile id to update")
    update_parser.add_argument("--name", type=str, help="qos profile name")
    update_parser.add_argument("--latency", type=float, help="qos profile latency")
    update_parser.add_argument("--jittermin", type=float, help="qos profile minimum jitter")
    update_parser.add_argument("--jittermax", type=float, help="qos profile maximum jitter")
    update_parser.add_argument("--trafficloss", type=float, help="qos profile traffic loss")
    update_parser.add_argument("--description", type=str, help="qos profile description")

    # delete
    delete_parser = subparsers.add_parser("delete", help="delete qos profile object")
    delete_parser_required = delete_parser.add_argument_group("required arguments")
    delete_parser_required.add_argument("--qosprofile", type=str, required=True, help="qos profile id to delete")

    args = vars(parser.parse_args())
    action_map = {
        "create": create,
        "read": read,
        "update": update,
        "delete": delete,
    }
    action_map[args['action']](config, args)

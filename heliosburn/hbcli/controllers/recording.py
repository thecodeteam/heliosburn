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
    url = config['url'] + "/api/recording/"

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
    url = config['url'] + "/api/recording/"

    if (args['all'] is False) and (args['recording'] is None):
        print("No recording(s) specified to read. Use -h to see usage.")
        return

    params = {}

    if (args['recording'] is not None) and (args['all'] is False):
        url += args['recording'] + "/"
        if args['traffic'] is True:
            url += "traffic/"
        if args['start'] is not None:
            params['start'] = args['start']
        if args['offset'] is not None:
            params['offset'] = args['offset']

    token = auth.get_token(config)
    r = requests.get(url, params=params, headers={"X-Auth-Token": token})
    if r.status_code != 200:
        print("API returned status code %s" % (r.status_code))
        sys.exit(1)
    else:
        pp.pprint(json.loads(r.content))


def update(config, args):
    url = config['url'] + "/api/recording/" + args['recording'] + "/"

    data = {}

    if args['name'] is not None:
        data['name'] = args['name']

    if args['description'] is not None:
        data['description'] = args['description']

    token = auth.get_token(config)
    r = requests.put(url, data=json.dumps(data), headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def delete(config, args):
    url = config['url'] + "/api/recording/" + args['recording'] + "/"
    token = auth.get_token(config)
    r = requests.delete(url, headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def start(config, args):
    url = config['url'] + "/api/recording/" + args['recording'] + "/start/"
    token = auth.get_token(config)
    r = requests.get(url, headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def stop(config, args):
    url = config['url'] + "/api/recording/" + args['recording'] + "/start/"
    token = auth.get_token(config)
    r = requests.get(url, headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def main(config, args):
    description = "Interact with recording objects."
    m = re.match(r'^.*\.(.*)$', __name__)
    controller_name = m.groups()[0]
    del sys.argv[1]
    parser = argparse.ArgumentParser(prog="%s %s" % (sys.argv[0], controller_name), description=description)
    subparsers = parser.add_subparsers(dest="action")

    # create
    create_parser = subparsers.add_parser("create", help="create recording object")
    create_parser_required = create_parser.add_argument_group("required arguments")
    create_parser_required.add_argument("--name", type=str, required=True, help="recording name")
    create_parser.add_argument("--description", type=str, help="recording description")

    # read
    read_parser = subparsers.add_parser("read", help="read recording object(s)")
    read_parser.add_argument("--all", action="store_const", const=True, default=False, help="read all recordings")
    read_parser.add_argument("--recording", type=str, help="ID of recording to read")
    read_parser_traffic = read_parser.add_argument_group("optional traffic-retrieval arguments")
    read_parser_traffic.add_argument("--traffic", action="store_const", const=True, default=False, help="include traffic for recording")
    read_parser_traffic.add_argument("--start", type=int, help="show traffic starting at N")
    read_parser_traffic.add_argument("--offset", type=int, help="read N traffic beyond --start")

    # update
    update_parser = subparsers.add_parser("update", help="update existing recording object")
    update_parser_required = update_parser.add_argument_group("required arguments")
    update_parser_required.add_argument("--recording", type=str, required=True, help="recording id to update")
    update_parser.add_argument("--name", type=str, help="recording name")
    update_parser.add_argument("--description", type=str, help="recording description")

    # delete
    delete_parser = subparsers.add_parser("delete", help="delete recording object")
    delete_parser_required = delete_parser.add_argument_group("required arguments")
    delete_parser_required.add_argument("--recording", type=str, required=True, help="recording id to delete")

    # start
    start_parser = subparsers.add_parser("start", help="start a recording")
    start_parser_required = start_parser.add_argument_group("required arguments")
    start_parser_required.add_argument("--recording", type=str, required=True, help="recording id to start")

    # stop
    stop_parser = subparsers.add_parser("stop", help="stop a recording")
    stop_parser_required = stop_parser.add_argument_group("required arguments")
    stop_parser_required.add_argument("--recording", type=str, required=True, help="recording id to stop")

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

import argparse
import sys
import re
import json
import requests
from models import auth
import pprint


def create(config, args):
    url = config['url'] + "/api/user/"
    data = {
        "username": args['username'],
        "password": args['password'],
        "email": args['email'],
    }
    if args['admin'] is not None:
        if args['admin'] == "yes":
            data['roles'] = ["admin"]
        else:
            data['roles'] = ["standard"]
    token = auth.get_token(config)
    r = requests.post(url, headers={"X-Auth-Token": token}, data=json.dumps(data))
    print("API returned status code %s" % (r.status_code))


def read(config, args):
    pp = pprint.PrettyPrinter()
    url = config['url'] + "/api/user/"
    if (args['all'] is False) and (args['username'] is None):
        print("No user object(s) specified to read. Use -h to see usage.")
        return
    elif args['all'] is True:
        token = auth.get_token(config)
        r = requests.get(url, headers={"X-Auth-Token": token})
        if r.status_code != 200:
            print("API returned status code %s" % (r.status_code))
            sys.exit(1)
        else:
            pp.pprint(json.loads(r.content))
    elif args['username'] is not None:
        url += args['username'] + "/"
        token = auth.get_token(config)
        r = requests.get(url, headers={"X-Auth-Token": token})
        if r.status_code != 200:
            print("API returned status code %s" % (r.status_code))
            sys.exit(1)
        else:
            pp.pprint(json.loads(r.content))


def update(config, args):
    url = config['url'] + "/api/user/" + args['username'] + "/"
    data = {}
    if args['password'] is not None:
        data['password'] = args['password']
    if args['email'] is not None:
        data['email'] = args['email']
    if args['admin'] is not None:
        if args['admin'] == "yes":
            data['roles'] = ["admin"]
        else:
            data['roles'] = ["standard"]

    token = auth.get_token(config)
    r = requests.put(url, data=json.dumps(data), headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def delete(config, args):
    url = config['url'] + "/api/user/" + args['username'] + "/"
    token = auth.get_token(config)
    r = requests.delete(url, headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def main(config, args):
    description = "Interact with user objects."
    m = re.match(r'^.*\.(.*)$', __name__)
    controller_name = m.groups()[0]
    del sys.argv[1]
    parser = argparse.ArgumentParser(prog="%s %s" % (sys.argv[0], controller_name), description=description)
    subparsers = parser.add_subparsers(dest="action")
    
    # create 
    create_parser = subparsers.add_parser("create", help="create user object")
    create_parser_required = create_parser.add_argument_group("required arguments")
    create_parser_required.add_argument("--username", type=str, required=True, help="username of new user")
    create_parser_required.add_argument("--email", type=str, required=True, help="email of new user")
    create_parser_required.add_argument("--password", type=str, required=True, help="password of new user")
    create_parser_required.add_argument("--admin", choices=("yes","no"), required=True, help="set new user as admin")

    # read
    read_parser = subparsers.add_parser("read", help="read user object(s)")
    read_parser.add_argument("--username", type=str, help="username to read")
    read_parser.add_argument("--all", action="store_const", const=True, default=False, help="Display all user objects")

    # update 
    update_parser = subparsers.add_parser("update", help="update existing user object")
    update_parser_required = update_parser.add_argument_group("required arguments")
    update_parser_required.add_argument("--username", type=str, required=True, help="username to update")
    update_parser.add_argument("--email", type=str, help="email of user")
    update_parser.add_argument("--password", type=str, help="password of user")
    update_parser.add_argument("--admin", choices=("yes","no"), help="set user as admin")

    # delete
    delete_parser = subparsers.add_parser("delete", help="delete user object")
    delete_parser_required = delete_parser.add_argument_group("required arguments")
    delete_parser_required.add_argument("--username", type=str, required=True, help="username to delete")
    
    args = vars(parser.parse_args())
    action_map = {
        "create": create,
        "read": read,
        "update": update,
        "delete": delete,
    }
    action_map[args['action']](config, args)

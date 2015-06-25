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
       "response_triggers": [],
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
        profiles = json.loads(r.content)
        if "profiles" not in profiles:  # Put single responses in an array, the same way --all behaves
            profiles = {"profiles": [profiles, ]}

        # Step through response triggers in profiles, and append the 'number' key to indicate their sequence in the array
        for profile in profiles['profiles']:
            if "response_triggers" in profile:
                trigger_num = 0
                for response_trigger in profile['response_triggers']:
                    response_trigger['position'] = trigger_num
                    trigger_num += 1

        pp.pprint(profiles)


def update(config, args):
    url = config['url'] + "/api/serveroverload/" + args['serveroverload'] + "/"

    data = {}

    if args['name'] is not None:
        data['name'] = args['name']

    if args['description'] is not None:
        data['description'] = args['description']

    update_function = False
    function = {}

    if args['functiontype'] is not None:
        function['type'] = args['functiontype']
        update_function = True

    if args['functionexpvalue'] is not None:
        function['expValue'] = args['functionexpvalue']
        update_function = True

    if args['functiongrowthrate'] is not None:
        function['growthRate'] = args['functiongrowthrate']
        update_function = True

    if update_function is True:  # verify they provided all the pieces needed to update a function
        try:
            assert "type" in function
            assert "expValue" in function
            assert "growthRate" in function
            data['function'] = function
        except AssertionError:
            print("To update a function, you must provide the type, expvalue, and growthrate together.")
            sys.exit(1)

    token = auth.get_token(config)
    r = requests.put(url, data=json.dumps(data), headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def deletetrigger(config, args):
    url = config['url'] + "/api/serveroverload/" + args['serveroverload'] + "/"
    token = auth.get_token(config)
    r = requests.get(url, headers={"X-Auth-Token": token})
    if r.status_code != 200:
        print("API returned status code %s" % (r.status_code))
        sys.exit(1)
    profile = json.loads(r.content)
    try:
        profile['response_triggers'].pop(args['position'])
    except IndexError:
        print("Position %s was invalid in the response triggers!" % (args['position']))
        sys.exit(1)
    r = requests.put(url, data=json.dumps(profile), headers={"X-Auth-Token": token})
    print("API returned status code %s" % (r.status_code))


def inserttrigger(config, args):
    url = config['url'] + "/api/serveroverload/" + args['serveroverload'] + "/"
    token = auth.get_token(config)
    r = requests.get(url, headers={"X-Auth-Token": token})
    if r.status_code != 200:
        print("API returned status code %s" % (r.status_code))
        sys.exit(1)
    profile = json.loads(r.content)
    response_trigger = {
        "fromLoad": args['fromload'],
        "toLoad": args['toload'],
        "actions": [{
            "type": args['actiontype'],
            "value": args['actionvalue'],
            "percentage": args['actionpercentage'],
        }]
    }
    profile['response_triggers'].insert(args['position'], response_trigger)
    r = requests.put(url, data=json.dumps(profile), headers={"X-Auth-Token": token})
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
    create_parser_required.add_argument("--name", type=str, required=True)
    create_parser_required.add_argument("--description", type=str, required=True)
    create_parser_required.add_argument("--functiontype", type=str, required=True)
    create_parser_required.add_argument("--functionexpvalue", type=str, required=True)
    create_parser_required.add_argument("--functiongrowthrate", type=str, required=True)

    # read
    read_parser = subparsers.add_parser("read", help="read serveroverload profile object(s)")
    read_parser.add_argument("--all", action="store_const", const=True, default=False, help="read all serveroverload profiles")
    read_parser.add_argument("--serveroverloadprofile", type=str, help="ID of serveroverload profile to read")

    # update
    update_parser = subparsers.add_parser("update", help="update existing serveroverload profile object")
    update_parser_required = update_parser.add_argument_group("required arguments")
    update_parser_required.add_argument("--serveroverload", type=str, required=True, help="serveroverload profile id to update")
    update_parser.add_argument("--name", type=str)
    update_parser.add_argument("--description", type=str)
    update_parser.add_argument("--functiontype", type=str)
    update_parser.add_argument("--functionexpvalue", type=int)
    update_parser.add_argument("--functiongrowthrate", type=float)

    # delete trigger
    delete_trigger_parser = subparsers.add_parser("deletetrigger", help="delete a response trigger from serveroverload profile object")
    delete_trigger_required = delete_trigger_parser.add_argument_group("required arguments")
    delete_trigger_required.add_argument("--serveroverload", type=str, required=True, help="serveroverload profile id to update")
    delete_trigger_required.add_argument("--position", type=int, required=True, help="position of trigger to delete")

    # insert trigger
    insert_trigger_parser = subparsers.add_parser("inserttrigger", help="insert a response trigger into serveroverload profile object")
    insert_trigger_required = insert_trigger_parser.add_argument_group("required arguments")
    insert_trigger_required.add_argument("--serveroverload", type=str, required=True, help="serveroverload profile id to update")
    insert_trigger_required.add_argument("--position", type=int, required=True, help="position to insert trigger at")
    insert_trigger_required.add_argument("--fromload", type=float, required=True)
    insert_trigger_required.add_argument("--toload", type=float, required=True)
    insert_trigger_required.add_argument("--actiontype", type=str, required=True)
    insert_trigger_required.add_argument("--actionvalue", type=str, required=True)
    insert_trigger_required.add_argument("--actionpercentage", type=float, required=True)

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
        "deletetrigger": deletetrigger,
        "inserttrigger": inserttrigger,
    }
    action_map[args['action']](config, args)

import requests
import json
import pdb
import sys


def get_token(config):
    pdb.set_trace()    
    login_url = config['url'] + "/api/auth/login/"
    data = {
        "username": config['user'],
        "password": config['pass'],
    }
    r = requests.post(login_url, data=json.dumps(data))
    if r.status_code != 200:
        print("Status code %s returned from %s, please verify your 'config' settings." % (r.status_code, login_url))
        sys.exit(1)
    elif r.status_code == 200:
        if 'x-auth-token' in r.headers:
            return r.headers['x-auth-token']
        else:
            print("X-Auth-Token not present in response from %s!" % (login_url))
            sys.exit(1)

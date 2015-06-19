import requests
import json
import sys
import pdb
import os


def get_token(config):
    """Return a valid token, attempting to re-use any token present in the config.
    """
    if "token" in config:  # If an existing token is present, validate it and re-use
        r = requests.get(config['url'] + "/api/user/" + config['user'] + "/", headers={'X-Auth-Token': config['token']})
        if r.status_code == 200:
            return config['token']
        
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
            config['token'] = r.headers['x-auth-token']
            f = open(os.environ['HOME'] + "/.hbclirc", "w")
            f.write(json.dumps(config))
            f.close()
            return r.headers['x-auth-token']
        else:
            print("X-Auth-Token not present in response from %s!" % (login_url))
            sys.exit(1)

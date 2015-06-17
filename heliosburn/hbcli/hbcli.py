import os
import sys
import json
from controllers import config
from controllers import session
from controllers import user
from IPython.core.debugger import Tracer


def readrc():
    """Attemps to acquire a config from the follow locations in order to return a dict():

    ENV variables:
        $HBAPIURL
        $HBAPIUSER
        $HBAPIPASS

    JSON in Files:
        1) $HOME/.hbclirc
        2) /etc/hbclirc
    Failures to parse a valid JSON will cause sys.exit(1)
    """

    if ("HBAPIURL" in os.environ) and ("HBAPIUSER" in os.environ) and ("HBAPIPASS" in os.environ):
        return {
            "url": os.environ['HBAPIURL'],
            "user": os.environ['HBAPIUSER'],
            "pass": os.environ['HBAPIPASS']
        }
    else:
        search_paths = []
        config = None

        if "HOME" in os.environ:
            search_paths.append(os.environ['HOME'] + "/.hbclirc")
        search_paths.append("/etc/hbclirc")

        for path in search_paths:
            if os.path.isfile(path) is False:
                continue
            else:
                f = open(path, 'r')
                config = f.read()
                f.close()
                try:
                    config = json.loads(config)
                    break
                except ValueError as e:
                    print("Unable to parse %s, error: %s" % (path, e))
                    sys.exit(1)

        if config is None:
            print("Unable to load configuration from environment or files, please set the ENV or create a valid configuration file.")
            sys.exit(1)
        else:
            return config


def main():
    help = """
    usage: %s <command> [arguments]

    Commands:
        config    - adjust hbcli configuration
        user      - interact with users
        session   - interact with sessions

    The argument '-h' can be used after a command for detailed usage help.

    """ % sys.argv[0]
    if (len(sys.argv) < 2) or (sys.argv[1] == '-h'):
        print(help)
        sys.exit(0)


    f_map = {
        "config": config.main,
        "session": session.main,
        "user": user.main,
    }

    if sys.argv[1] != "config":
        rc = readrc()
    else:
        rc = None

    if sys.argv[1] in f_map:
        f_map[sys.argv[1]](rc, sys.argv)
    else:
        print(help)
        sys.exit(0)
    return 0

if __name__ == "__main__":
    main()

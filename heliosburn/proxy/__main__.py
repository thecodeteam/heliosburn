
import argparse
from settings import Common
from service.server import HBProxyServer


def get_arg_parser():

    description = " Helios Burn Service Controller:  \n\n"

    parser = argparse.ArgumentParser(description=description)


    parser.add_argument('--redis_mgmt',
                        action="store_true",
                        dest='redis_mgmt',
                        help='If set will subscribe to a given REDIS' +
                        ' channel for proxy mgmt commands' +
                        ' Default: true')

    parser.add_argument('--redis_host',
                        dest='redis_host',
                        help='If the proxy mgmt interface is listening' +
                        ' on a tcp socket, this option will set the' +
                        ' address on which to listen.')

    parser.add_argument('--redis_port',
                        dest='redis_port',
                        help='If the proxy mgmt interface is listening' +
                        ' on a tcp socket, this option will set the port' +
                        ' on which to listen.')

    parser.add_argument('--request_channel',
                        dest='request_channel',
                        help='If the proxy mgmt interface is set to use' +
                        'redis, this option will set the channel to' +
                        ' which it should subscribe.')

    parser.add_argument('--response_channel',
                        dest='response_channel',
                        help='If the proxy mgmt interface is set to use ' +
                        ' redis, this option will set the channel to ' +
                        ' which it should publish.')

    parser.add_argument('--test',
                        action="store_true",
                        dest='run_tests',
                        help='If set will run all proxy tests' +
                        ' Default: false')

    return parser


def main():
    """
    Entry point for starting the proxy server
    """
    args = get_arg_parser().parse_args()

    config = Common.PROXY

    if args.redis_mgmt:
        if args.redis_address:
            config['redis_host'] = args.redis_host
        if args.redis_port:
            config['redis_port'] = args.redis_port
        if args.request_channel:
            config['control_pub_queue'] = args.request_channel
        if args.response_channel:
            config['control_sub_queue'] = args.response_channel


    proxy_server = HBProxyServer(configs=config)
    if args.run_tests:
        proxy_server.test()
    else:
        proxy_server.run()

if __name__ == "__main__":
    main()


import argparse
from settings import Common
from service.server import HBProxyServer


def get_arg_parser():

    description = " Helios Burn Service Controller:  \n\n"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--tcp_mgmt',
                        action="store_true",
                        dest='tcp_mgmt',
                        help='If set will listen for proxy mgmt commands on' +
                        ' a TCP port as well as subscribe to the request' +
                        ' channel. Default: false')

    parser.add_argument('--tcp_address',
                        dest='tcp_mgmt_address',
                        help='If the proxy mgmt interface is listening ' +
                        ' on a tcp socket, this option will set the address' +
                        ' on which to listen.')

    parser.add_argument('--tcp_port',
                        dest='tcp_mgmt_port',
                        help='If the proxy mgmt interface is listening ' +
                        ' on a tcp socket, this option will set the port' +
                        ' on which to listen.')

    parser.add_argument('--redis_mgmt',
                        action="store_true",
                        dest='redis_mgmt',
                        help='If set will subscribe to a given REDIS' +
                        ' channel for proxy mgmt commands' +
                        ' Default: true')

    parser.add_argument('--redis_address',
                        dest='redis_address',
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

    config = Common['PROXY']

    proxy_address = config['proxy_address']
    proxy_port = config['proxy_port']
    upstream_host = config['upstream_address']
    upstream_port = config['upstream_port']
    redis_address = config['redis_host']
    redis_port = config['redis_port']
    redis_db = config['redis_db']
    mongo_address = config['mongo_host']
    mongo_port = config['mongo_port']
    mongo_db = config['mongo_db']
    traffic_pub_queue = config['heliosburn.traffic']
    traffic_sub_queue = config['heliosburn.traffic']
    control_pub_queue = config['control_pub_queue']
    control_sub_queue = config['control_sub_queue']

    if args.redis_mgmt:
        if args.redis_address:
            redis_address = args.redis_address
        if args.redis_port:
            redis_port = args.redis_address
        if args.request_channel:
            control_pub_queue = args.request_channel
        if args.response_channel:
            control_sub_queue = args.response_channel

    plugins = config['plugins']

    proxy_server = HBProxyServer(proxy_address=proxy_address,
                                 proxy_port=proxy_port,
                                 upstream_host=upstream_host,
                                 upstream_port=upstream_port,
                                 redis_address=redis_address,
                                 redis_port=redis_port,
                                 redis_db=redis_db,
                                 mongo_address=mongo_address,
                                 mongo_port=mongo_port,
                                 mongo_db=mongo_db,
                                 control_pub_queue=control_pub_queue,
                                 control_sub_queue=control_sub_queue,
                                 traffic_pub_queue=traffic_pub_queue,
                                 traffic_sub_queue=traffic_sub_queue,
                                 plugins=plugins)
    if args.run_tests:
        proxy_server.test()
    else:
        proxy_server.run()

if __name__ == "__main__":
    main()


import yaml
import argparse
from controller.service import HBServiceController


def get_config(config_path):
    with open(config_path, 'r+') as config_file:
        config = yaml.load(config_file.read())

    return config


def get_arg_parser():

    description = " Helios Burn Service Controller:  \n\n"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--config_path',
                        default="./config.yaml",
                        dest='config_path',
                        help='Path to output config file. Default: '
                        + ' ./config.yaml')

    parser.add_argument('--tcp_mgmt',
                        action="store_true",
                        dest='tcp_mgmt',
                        help='If set will listen for proxy mgmt commands on'
                        + ' a TCP port as well as subscribe to the request'
                        + ' channel. Default: false')

    parser.add_argument('--tcp_address',
                        dest='tcp_mgmt_address',
                        help='If the proxy mgmt interface is listening '
                        + ' on a tcp socket, this option will set the address'
                        + ' on which to listen.')

    parser.add_argument('--tcp_port',
                        dest='tcp_mgmt_port',
                        help='If the proxy mgmt interface is listening '
                        + ' on a tcp socket, this option will set the port'
                        + ' on which to listen.')

    parser.add_argument('--redis_mgmt',
                        action="store_true",
                        dest='redis_mgmt',
                        help='If set will subscribe to a given REDIS'
                        + ' channel for proxy mgmt commands'
                        + ' Default: true')

    parser.add_argument('--redis_address',
                        dest='redis_address',
                        help='If the proxy mgmt interface is listening '
                        + ' on a tcp socket, this option will set the address'
                        + ' on which to listen.')

    parser.add_argument('--redis_port',
                        dest='redis_port',
                        help='If the proxy mgmt interface is listening '
                        + ' on a tcp socket, this option will set the port'
                        + ' on which to listen.')

    parser.add_argument('--request_channel',
                        dest='request_channel',
                        help='If the proxy mgmt interface is set to use redis'
                        + ', this option will set the channel to which it '
                        + ' should subscribe.')

    parser.add_argument('--response_channel',
                        dest='response_channel',
                        help='If the proxy mgmt interface is set to use redis'
                        + ', this option will set the channel to which it '
                        + ' should publish.')

    parser.add_argument('--test',
                        action="store_true",
                        dest='run_tests',
                        help='If set will run all proxy tests'
                        + ' Default: false')

    return parser


def main():
    """
    Entry point for starting the proxy
    """
    args = get_arg_parser().parse_args()
    config_path = args.config_path

    config = get_config(config_path)
    proxy_config = config['proxy']
    mgmt_config = config['mgmt']

    bind_address = proxy_config['bind_address']
    protocols = proxy_config['protocols']
    upstream_host = proxy_config['upstream']['address']
    upstream_port = proxy_config['upstream']['port']
    tcp_mgmt_address = mgmt_config['tcp']['address']
    tcp_mgmt_port = mgmt_config['tcp']['port']
    redis_address = mgmt_config['redis']['address']
    redis_port = mgmt_config['redis']['port']
    request_channel = mgmt_config['redis']['request_channel']
    response_channel = mgmt_config['redis']['response_channel']

    if args.tcp_mgmt:
        if args.tcp_mgmt_address:
            tcp_mgmt_address = args.tcp_mgmt_address

        if args.tcp_mgmt_port:
            tcp_mgmt_port = args.tcp_mgmt_port

    if args.redis_mgmt:
        if args.redis_address:
            redis_address = args.redis_address
        if args.redis_port:
            redis_port = args.redis_address
        if args.request_channel:
            request_channel = args.request_channel
        if args.response_channel:
            response_channel = args.response_channel

    plugins = get_config("./modules.yaml")
    proxy_controller = HBServiceController(bind_address, protocols,
                                           upstream_host, upstream_port,
                                           args.redis_mgmt, redis_address,
                                           redis_port, request_channel,
                                           response_channel, args.tcp_mgmt,
                                           tcp_mgmt_address, tcp_mgmt_port,
                                           plugins)
    if args.run_tests:
        proxy_controller.test()
    else:
        proxy_controller.run()

if __name__ == "__main__":
    main()

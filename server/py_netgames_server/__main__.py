import argparse
import http
import logging
import os

from py_netgames_server.websocket_server_builder import WebSocketServerBuilder


def setup_logger(log_level):
    logging.basicConfig(format='%(name)s %(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(log_level)


def setup_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        help="Debug websocket connections",
        action="store_const", dest="log_level", const=logging.DEBUG,
        default=logging.ERROR
    )
    parser.add_argument(
        '--host',
        help="Server host",
        dest="host", default="0.0.0.0"
    )
    parser.add_argument(
        '-p', '--port',
        help="Server port",
        dest="port", default=8765
    )
    return parser


async def health_check(path, request_headers):
    if path == "/health":
        return http.HTTPStatus.OK, [], b"OK\n"

if __name__ == '__main__':
    args = setup_arg_parser().parse_args()
    setup_logger(args.log_level)
    WebSocketServerBuilder().serve(args.host, args.port, health_check)

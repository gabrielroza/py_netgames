import logging

from py_netgames_server.websocket_server_builder import WebSocketServerBuilder


def setup_logger():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


if __name__ == '__main__':
    setup_logger()
    WebSocketServerBuilder().serve()

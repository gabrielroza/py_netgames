import logging
import sys

from main_loop import MainLoop


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))


if __name__ == '__main__':
    setup_logger()
    MainLoop()

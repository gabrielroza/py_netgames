import asyncio
import logging
import sys
import uuid

from client.cliente.asynciobasedproxy import AsyncIoBasedProxy


class Actor(AsyncIoBasedProxy):

    def _match_started(self):
        pass

    def _receive_move(self, payload: any):
        pass


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))


async def coroutine():
    actor = Actor()
    await actor.connect("localhost:8765")
    await actor.request_match("Gabriel", uuid.uuid4(), 2)
    await actor.request_match("Gabriel 2", uuid.uuid4(), 2)


if __name__ == '__main__':
    setup_logger()
    asyncio.run(coroutine())

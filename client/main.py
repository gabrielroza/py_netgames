import asyncio
import logging
import sys
import uuid

from client.cliente.asynciobasedproxy import AsyncIoBasedProxy


class Actor(AsyncIoBasedProxy):
    _logger: logging.Logger

    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger("cliente.Actor")

    async def _match_started(self, position: int):
        self._logger.info(f"Match started with position {position}")

    async def _receive_move(self, payload: any):
        self._logger.info(f"Move received {payload}")


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))


async def coroutine():
    actor = Actor()
    await actor.connect("localhost:8765")
    await actor.request_match("Gabriel", uuid.UUID("c0ec55a4-3c5d-4c78-a246-2c1c2cfe8a50"), 2)
    return await actor.listen()

if __name__ == '__main__':
    setup_logger()
    asyncio.get_event_loop().run_until_complete(coroutine())

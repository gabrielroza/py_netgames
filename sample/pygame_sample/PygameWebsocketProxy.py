import asyncio
import threading
from asyncio import AbstractEventLoop

import pygame
from websockets import client, WebSocketClientProtocol

CONNECTED = pygame.event.custom_type()


class PygameWebsocketProxy:
    _loop: AbstractEventLoop
    _websocket: WebSocketClientProtocol

    def __init__(self) -> None:
        super().__init__()
        self._loop = asyncio.get_event_loop()
        self._pygame = pygame

    def connect(self, address: str) -> None:
        async def async_connect():
            self._websocket = await client.connect("ws://" + address)
            print(self._websocket)
            print(pygame)
            return pygame.event.post(pygame.event.Event(CONNECTED, message={}))

        self._run(target=async_connect)

    def _run(self, target):
        thread = threading.Thread(target=lambda: self._loop.run_until_complete(target()))
        thread.start()

    def _run_forever(self, target):
        future = self._loop.create_future()
        thread = threading.Thread(target=lambda f: self._loop.run_until_complete(target(f)), args=future)
        thread.start()

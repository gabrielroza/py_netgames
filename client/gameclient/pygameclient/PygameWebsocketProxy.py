import asyncio
import threading
from asyncio import AbstractEventLoop
from threading import Thread

import pygame
from websockets import client, WebSocketClientProtocol

CONNECTED = pygame.event.custom_type()
RECEIVED = pygame.event.custom_type()


class PygameWebsocketProxy:
    _thread: Thread
    _loop: AbstractEventLoop
    _websocket: WebSocketClientProtocol

    def __init__(self) -> None:
        super().__init__()
        self._loop = asyncio.new_event_loop()

        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            loop.run_forever()

        self._thread = threading.Thread(target=start_background_loop, args=(self._loop,))
        self._thread.start()
        self._pygame = pygame

    def connect(self, address: str) -> None:
        async def async_connect():
            self._websocket = await client.connect("ws://" + address)
            return pygame.event.post(pygame.event.Event(CONNECTED, message={}))

        self._run(target=async_connect)

    def send(self, message: str) -> None:
        async def async_send():
            await self._websocket.send(message)

        self._run(target=async_send)

    def listen(self) -> None:
        async def async_listen():
            async for message in self._websocket:
                pygame.event.post(pygame.event.Event(RECEIVED, message=message))

        self._run(target=async_listen)

    def _run(self, target):
        asyncio.run_coroutine_threadsafe(target(), self._loop)

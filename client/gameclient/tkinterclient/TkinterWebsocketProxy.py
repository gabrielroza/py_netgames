import asyncio
import threading
from asyncio import AbstractEventLoop
from typing import List

from model.messaging.deserializer import WebhookPayloadDeserializer
from websockets import client
from websockets.legacy.client import WebSocketClientProtocol

from gameclient.tkinterclient.TkinterWebsocketListener import TkinterWebsocketListener


class TkinterWebsocketProxy:
    __websocket: WebSocketClientProtocol
    __deserializer: WebhookPayloadDeserializer
    __loop: AbstractEventLoop
    __listeners: List[TkinterWebsocketListener]

    def __init__(self) -> None:
        super().__init__()
        self.__deserializer = WebhookPayloadDeserializer()
        self.__loop = asyncio.new_event_loop()

        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            loop.run_forever()

        self._thread = threading.Thread(target=start_background_loop, args=(self.__loop,))

        self.__listeners = []

    def __run_blocking(self, coroutine):
        return self.__loop.run_until_complete(coroutine)

    def connect(self, server_address: str = 'localhost:8765'):
        async def async_connect() -> WebSocketClientProtocol:
            return await client.connect("ws://" + server_address)

        self.__websocket = self.__run_blocking(async_connect())

    def disconnect(self):
        async def async_connect():
            await self.__websocket.close()
            self.__websocket = None

        self.__run_blocking(async_connect())

    def add_listener(self, listener: TkinterWebsocketListener):
        self.__listeners.append(listener)

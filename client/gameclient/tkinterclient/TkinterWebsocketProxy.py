import asyncio
from asyncio import AbstractEventLoop
from typing import Awaitable
from uuid import UUID

from model.messaging.deserializer import WebhookPayloadDeserializer
from websockets.legacy.client import WebSocketClientProtocol
from websockets import client, WebSocketClientProtocol

from gameclient.tkinterclient.TkinterWebsocketListener import TkinterWebsocketListener


class TkinterWebsocketProxy:
    _websocket: WebSocketClientProtocol
    _deserializer: WebhookPayloadDeserializer
    _loop: AbstractEventLoop

    def __init__(self) -> None:
        super().__init__()
        self.__deserializer = WebhookPayloadDeserializer()
        self._loop = asyncio.new_event_loop()

    def connect(self, address: str) -> None:
        async def async_connect() -> WebSocketClientProtocol:
            return await client.connect("ws://" + address)

        self._websocket = self._run_blocking(async_connect())

    def disconnect(self) -> None:
        async def async_disconnect():
            await self._websocket.close()

        self._run_blocking(async_disconnect())

    def request_match(self, game_id: UUID, amount_of_players: int):
        pass

    def send_move(self, match_id: UUID, payload: str) -> None:
        pass

    def listen(self, listener: TkinterWebsocketListener) -> None:
        pass

    def _run_blocking(self, coroutine):
        return self._loop.run_until_complete(coroutine)
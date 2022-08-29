import asyncio
import threading
from asyncio import AbstractEventLoop
from typing import List
from uuid import UUID

from model.messaging.deserializer import WebhookPayloadDeserializer
from model.messaging.message import MatchRequestMessage, MoveMessage
from model.messaging.webhook_payload import WebhookPayloadType
from websockets import client
from websockets.legacy.client import WebSocketClientProtocol

from gameclient.tkinterclient.TkinterWebsocketListener import TkinterWebsocketListener


class TkinterWebsocketProxy:
    _websocket: WebSocketClientProtocol
    _deserializer: WebhookPayloadDeserializer
    _loop: AbstractEventLoop
    _listeners: List[TkinterWebsocketListener]

    def __init__(self) -> None:
        super().__init__()
        self._deserializer = WebhookPayloadDeserializer()
        self._loop = asyncio.new_event_loop()

        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            loop.run_forever()

        self._thread = threading.Thread(target=start_background_loop, args=(self._loop,))
        self._thread.start()

        self._listeners = []

    def _run_blocking(self, coroutine):
        return asyncio.new_event_loop().run_until_complete(coroutine)

    def _run(self, target):
        asyncio.run_coroutine_threadsafe(target(), self._loop)

    def _send(self, message):
        async def async_send():
            try:
                await self._websocket.send(message)
            except Exception as e:
                print(e)

        self._run(async_send)

    def connect(self, server_address: str = 'localhost:8765'):
        async def async_connect() -> None:
            self._websocket = await client.connect("ws://" + server_address)
            self._listen()

        self._run(async_connect)

    def request_match(self, game_id: UUID, amount_of_players: int):
        self._send(MatchRequestMessage(game_id, amount_of_players).to_payload().to_json())

    def send_move(self, match_id: UUID, payload: str) -> None:
        self._send(MoveMessage(match_id, payload).to_payload().to_json())

    def disconnect(self):
        async def async_disconnect():
            await self._websocket.close()
            self._websocket = None

        self._run(async_disconnect)

    def add_listener(self, listener: TkinterWebsocketListener):
        self._listeners.append(listener)

    def _listen(self) -> None:
        async def async_listen():
            try:
                async for message in self._websocket:
                    message = self._deserializer.deserialize(message)
                    if WebhookPayloadType.MATCH_STARTED == message.type():
                        [listener.match_started(message) for listener in self._listeners]
                    elif WebhookPayloadType.MOVE == message.type():
                        [listener.receive_move(message) for listener in self._listeners]
            except Exception as e:
                print(e)

        self._run(target=async_listen)

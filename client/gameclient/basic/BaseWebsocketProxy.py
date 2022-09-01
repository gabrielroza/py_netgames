import asyncio
import threading
from abc import ABC
from asyncio import AbstractEventLoop
from typing import Dict
from uuid import UUID

from model.messaging.deserializer import WebhookPayloadDeserializer
from model.messaging.message import MoveMessage, MatchRequestMessage, MatchStartedMessage
from model.messaging.webhook_payload import WebhookPayloadType
from websockets import client, WebSocketClientProtocol

from gameclient.id.IdentifierFileGenerator import IdentifierFileGenerator


class BaseWebsocketProxy(ABC):
    _thread: threading.Thread
    _loop: AbstractEventLoop
    _websocket: WebSocketClientProtocol
    _deserializer: WebhookPayloadDeserializer
    _game_id: UUID

    def __init__(self, game_id: UUID = None) -> None:
        super().__init__()
        self._loop = asyncio.new_event_loop()
        self.__deserializer = WebhookPayloadDeserializer()
        self._game_id = game_id if game_id else IdentifierFileGenerator().get_or_create_identifier()

        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            loop.run_forever()

        self._thread = threading.Thread(target=start_background_loop, args=(self._loop,))
        self._thread.start()

    def _receive_match_start(self, match: MatchStartedMessage):
        raise NotImplementedError()

    def _receive_move(self, move: MoveMessage):
        raise NotImplementedError()

    def _disconnection(self):
        raise NotImplementedError()

    def _connection_success(self):
        raise NotImplementedError()

    def _error(self, error: Exception):
        raise NotImplementedError()

    def _match_requested_success(self):
        raise NotImplementedError()

    def _move_sent_success(self):
        raise NotImplementedError()

    def connect(self, address: str) -> None:
        async def async_connect():
            try:
                self._websocket = await client.connect("ws://" + address)
                self._listen()
                self._connection_success()
            except Exception as e:
                return self._error(e)

        self._run(target=async_connect)

    def disconnect(self) -> None:
        async def async_disconnect():
            try:
                await self._websocket.close()
                return self._disconnection()
            except Exception as e:
                return self._error(e)

        self._run(target=async_disconnect)

    def request_match(self, amount_of_players: int):
        self._send(MatchRequestMessage(self._game_id, amount_of_players).to_payload().to_json(),
                   self._match_requested_success)

    def send_move(self, match_id: UUID, payload: Dict[str, any]) -> None:
        self._send(MoveMessage(match_id, payload).to_payload().to_json(), self._move_sent_success)

    def _send(self, message: str, on_success) -> None:
        async def async_send():
            try:
                await self._websocket.send(message)
                return on_success()
            except Exception as e:
                return self._error(e)

        self._run(target=async_send)

    def _listen(self) -> None:
        async def async_listen():
            try:
                async for message in self._websocket:
                    message = self.__deserializer.deserialize(message)
                    if WebhookPayloadType.MATCH_STARTED == message.type():
                        self._receive_match_start(message)
                    elif WebhookPayloadType.MOVE == message.type():
                        self._receive_move(message)
                self._disconnection()
            except Exception as e:
                return self._error(e)

        self._run(target=async_listen)

    def _run(self, target):
        asyncio.run_coroutine_threadsafe(target(), self._loop)

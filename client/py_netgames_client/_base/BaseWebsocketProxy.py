import asyncio
import threading
import warnings
from abc import ABC
from asyncio import AbstractEventLoop
from concurrent.futures import Future
from typing import Dict, Optional
from uuid import UUID

from py_netgames_model.messaging.deserializer import WebhookPayloadDeserializer
from py_netgames_model.messaging.message import MoveMessage, MatchRequestMessage, MatchStartedMessage
from py_netgames_model.messaging.webhook_payload import WebhookPayloadType
from py_netgames_server.websocket_server_builder import WebSocketServerBuilder
from websockets import client, WebSocketClientProtocol

from py_netgames_client.id.IdentifierFileGenerator import IdentifierFileGenerator


class BaseWebsocketProxy(ABC):
    _thread: threading.Thread
    _loop: AbstractEventLoop
    _websocket: Optional[WebSocketClientProtocol]
    _deserializer: WebhookPayloadDeserializer
    _game_id: UUID

    def __init__(self, game_id: UUID = None) -> None:
        super().__init__()
        self._loop = asyncio.new_event_loop()
        self.__deserializer = WebhookPayloadDeserializer()
        self._game_id = game_id if game_id else IdentifierFileGenerator().get_or_create_identifier()
        self._websocket = None

        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            loop.run_forever()

        self._thread = threading.Thread(target=start_background_loop, args=(self._loop,))
        self._thread.start()

    def _open(self):
        return self._websocket and self._websocket.open

    def _closed(self):
        return not self._open()

    def send_connect(self, address: str, run_server_on_miss: bool = True) -> None:

        if self._open():
            return warnings.warn(f"Call to send_connect when connection is already active.", stacklevel=2)

        async def async_connect():

            async def attempt_connection():
                self._websocket = await client.connect("ws://" + address)
                self._listen()
                self._connection_success()

            try:
                await attempt_connection()
            except ConnectionRefusedError as connection_refused_error:
                if run_server_on_miss:
                    await WebSocketServerBuilder().async_serve()
                    await attempt_connection()
                else:
                    return self._error(connection_refused_error)
            except Exception as e:
                return self._error(e)

        self._run(target=async_connect)

    def send_disconnect(self) -> None:

        if self._closed():
            return warnings.warn(f"Call to send_disconnect when there is no active connection", stacklevel=2)

        async def async_disconnect():
            try:
                await self._websocket.close()
                return self._disconnection()
            except Exception as e:
                return self._error(e)

        self._run(target=async_disconnect)

    def send_match(self, amount_of_players: int) -> None:

        if self._closed():
            return warnings.warn(f"Call to send_match when there is no active connection", stacklevel=2)

        self._send(MatchRequestMessage(self._game_id, amount_of_players).to_payload().to_json(),
                   self._match_requested_success)

    def send_move(self, match_id: UUID, payload: Dict[str, any]) -> None:

        if self._closed():
            return warnings.warn(f"Call to send_move when there is no active connection", stacklevel=2)

        self._send(MoveMessage(match_id, payload).to_payload().to_json(), self._move_sent_success)

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

    def _run(self, target) -> Future:
        return asyncio.run_coroutine_threadsafe(target(), self._loop)

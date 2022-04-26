import abc
import asyncio
import logging
from abc import ABC
from logging import Logger
from uuid import UUID

import websockets
from model.messaging.message import MatchRequestMessage, MoveMessage
from websockets import WebSocketServerProtocol


class AsyncIoBasedProxy(ABC):
    _websocket: WebSocketServerProtocol
    _logger: Logger

    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger("cliente.Proxy")

    @abc.abstractmethod
    def _match_started(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def _receive_move(self, payload: any):
        raise NotImplementedError()

    async def connect(self, address: str):
        self._websocket = await websockets.connect("ws://" + address)
        self._logger.info("Connected to server")
        asyncio.create_task(self._listen())

    async def _listen(self):
        async for message in self._websocket:
            self._logger.debug(f"Message received: {message}")

    async def request_match(self, player_name: str, game_id: UUID, amount_of_players: int):
        payload = MatchRequestMessage(player_name, game_id, amount_of_players).to_payload().to_json()
        await self._send_message(payload)

    async def send_move(self, match_id: UUID, payload: any):
        payload = MoveMessage(match_id, payload).to_payload().to_json()
        await self._send_message(payload)

    async def disconnect(self):
        await self._websocket.disconnect()
        self._logger.info("Connection severed")

    async def end_match(self):
        await self.disconnect()

    async def _send_message(self, message: str):
        await self._websocket.send(message)
        self._logger.debug(f"Message sent: {message}")

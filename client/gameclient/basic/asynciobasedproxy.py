import abc
import logging
from abc import ABC
from logging import Logger
from uuid import UUID

import websockets
from model.messaging.deserializer import WebhookPayloadDeserializer
from model.messaging.message import MatchRequestMessage, MoveMessage
from model.messaging.webhook_payload import WebhookPayloadType
from websockets import WebSocketServerProtocol


class AsyncIoBasedProxy(ABC):
    __websocket: WebSocketServerProtocol
    __logger: Logger
    __deserializer: WebhookPayloadDeserializer

    def __init__(self) -> None:
        super().__init__()
        self.__logger = logging.getLogger("basic.Proxy")
        self.__deserializer = WebhookPayloadDeserializer()

    @abc.abstractmethod
    async def _match_started(self, position: int):
        raise NotImplementedError()

    @abc.abstractmethod
    async def _receive_move(self, payload: any):
        raise NotImplementedError()

    async def connect(self, address: str):
        self.__websocket = await websockets.connect("ws://" + address)
        self.__logger.info("Connected to server")

    async def listen(self):
        async for message in self.__websocket:
            self.__logger.info(f"Message received: {message}")
            message = self.__deserializer.deserialize(message)
            if WebhookPayloadType.MATCH_STARTED == message.type():
                await self._match_started(message.position)
            elif WebhookPayloadType.MOVE == message.type():
                await self._receive_move(message.payload)

    async def request_match(self, player_name: str, game_id: UUID, amount_of_players: int):
        payload = MatchRequestMessage(player_name, game_id, amount_of_players).to_payload().to_json()
        await self._send_message(payload)

    async def send_move(self, match_id: UUID, payload: str):
        payload = MoveMessage(match_id, payload).to_payload().to_json()
        await self._send_message(payload)

    async def disconnect(self):
        await self.__websocket.close()
        self.__logger.info("Connection severed")

    async def end_match(self):
        await self.disconnect()

    async def _send_message(self, message: str):
        await self.__websocket.send(message)
        self.__logger.info(f"Message sent: {message}")

import asyncio
import threading
from asyncio import AbstractEventLoop
from threading import Thread
from uuid import UUID

import pygame
from model.messaging.deserializer import WebhookPayloadDeserializer
from model.messaging.message import MoveMessage, MatchRequestMessage
from model.messaging.webhook_payload import WebhookPayloadType
from websockets import client, WebSocketClientProtocol

CONNECTED = pygame.event.custom_type()
CONNECTION_ERROR = pygame.event.custom_type()
RECEIVED = pygame.event.custom_type()
MATCH_STARTED = pygame.event.custom_type()
MOVE = pygame.event.custom_type()
DISCONNECT = pygame.event.custom_type()


class PygameWebsocketProxy:
    _thread: Thread
    _loop: AbstractEventLoop
    _websocket: WebSocketClientProtocol
    _deserializer: WebhookPayloadDeserializer

    def __init__(self) -> None:
        super().__init__()
        self._loop = asyncio.new_event_loop()
        self.__deserializer = WebhookPayloadDeserializer()

        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            loop.run_forever()

        self._thread = threading.Thread(target=start_background_loop, args=(self._loop,))
        self._thread.start()
        self._pygame = pygame

    def connect(self, address: str) -> None:
        async def async_connect():
            try:
                self._websocket = await client.connect("ws://" + address)
                return pygame.event.post(pygame.event.Event(CONNECTED, message={}))
            except Exception as e:
                return pygame.event.post(pygame.event.Event(CONNECTION_ERROR, message=e))

        self._run(target=async_connect)

    def disconnect(self) -> None:
        async def async_disconnect():
            try:
                self._websocket.close()
                return pygame.event.post(pygame.event.Event(DISCONNECT, message={}))
            except Exception as e:
                return pygame.event.post(pygame.event.Event(CONNECTION_ERROR, message=e))

        self._run(target=async_disconnect)

    def request_match(self, player_name: str, game_id: UUID, amount_of_players: int):
        self._send(MatchRequestMessage(player_name, game_id, amount_of_players).to_payload().to_json())

    def send_move(self, match_id: UUID, payload: any) -> None:
        self._send(MoveMessage(match_id, payload).to_payload().to_json())

    def _send(self, message: str) -> None:
        async def async_send():
            try:
                await self._websocket.send(message)
            except Exception as e:
                return pygame.event.post(pygame.event.Event(CONNECTION_ERROR, message=e))

        self._run(target=async_send)

    def listen(self) -> None:
        async def async_listen():
            try:
                async for message in self._websocket:
                    message = self.__deserializer.deserialize(message)
                    if WebhookPayloadType.MATCH_STARTED == message.type():
                        pygame.event.post(pygame.event.Event(MATCH_STARTED, message=message.position))
                    elif WebhookPayloadType.MOVE == message.type():
                        pygame.event.post(pygame.event.Event(MOVE, message=message.payload))
            except Exception as e:
                return pygame.event.post(pygame.event.Event(CONNECTION_ERROR, message=e))

        self._run(target=async_listen)

    def _run(self, target):
        asyncio.run_coroutine_threadsafe(target(), self._loop)

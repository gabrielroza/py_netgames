import dataclasses
import logging
from logging import Logger
from typing import Type, Dict, Callable, TypeVar, Set, Awaitable

from model.messaging.message import MatchRequestMessage, Message, MatchStartedMessage, MoveMessage
from websockets import WebSocketServerProtocol

from match import Match

T = TypeVar('T', bound=Message)


class Server:
    __matches: Set[Match]
    __handle_map: Dict[Type[T], Callable[[T, WebSocketServerProtocol], Awaitable[None]]]
    __logger: Logger

    def __init__(self):
        super().__init__()
        self.__matches = set()
        self.__handle_map = {
            MatchRequestMessage: self.__start_match,
            MoveMessage: self.__move
        }
        self.__logger = logging.getLogger("server.Server")

    async def handle_message(self, message: Message, sender: WebSocketServerProtocol):
        await self.__handle_map[message.__class__](message, sender)

    async def handle_disconnect(self, disconnected_socket: WebSocketServerProtocol):
        try:
            match = next(match for match in self.__matches if disconnected_socket in match.players)
            [await websocket.close(reason="Player disconnected") for websocket in match.players - {disconnected_socket}]
            self.__matches.remove(match)
            self.__logger.info(f"Dropped match with {len(match.players)} connections after player disconnected.")
        except StopIteration:
            self.__logger.error(f"No match found for disconnected websocket.")

    async def __start_match(self, message: MatchRequestMessage, sender: WebSocketServerProtocol):
        try:
            existing_match = next(match for match in self.__matches if match.accepting_players(message.game_id))
            self.__matches.remove(existing_match)
            match = dataclasses.replace(existing_match, players=frozenset([*existing_match.players, sender]))
            self.__matches.add(match)
            if not match.accepting_players(message.game_id):
                [await self.__send(MatchStartedMessage(match.id, position), {websocket}) for position, websocket in
                 enumerate(match.players)]
        except StopIteration:
            match = Match.create(message, sender)
            self.__matches.add(match)

    async def __move(self, message: MoveMessage, sender: WebSocketServerProtocol):
        try:
            match = next(match for match in self.__matches if match.id == message.match_id)
            await self.__send(message, match.players - {sender})
        except StopIteration:
            self.__logger.error(f"Match not found for match_id {message.match_id}")

    async def __send(self, message: Message, recipients: [WebSocketServerProtocol]):
        [await websocket.send(message.to_payload().to_json()) for websocket in recipients]

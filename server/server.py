import dataclasses
from typing import Type, Dict, Callable, TypeVar, Set, Awaitable

from websockets import WebSocketServerProtocol

from model.domain.game import Game
from model.domain.match import Match
from model.messaging.message import MatchRequestMessage, Message, MatchStartedMessage

T = TypeVar('T', bound=Message)


class Server:
    __matches: Set[Match]
    __games: Set[Game]
    __handle_table: Dict[Type[T], Callable[[T, WebSocketServerProtocol], Awaitable[None]]]

    def __init__(self):
        super().__init__()
        self.__games = set()
        self.__matches = set()
        self.__handle_table = {
            MatchRequestMessage: self.start_match
        }

    async def handle(self, message: Message, websocket: WebSocketServerProtocol):
        await self.__handle_table[message.__class__](message, websocket)

    async def start_match(self, message: MatchRequestMessage, websocket: WebSocketServerProtocol):
        try:
            existing_match = next(match for match in self.__matches if match.accepting_players(message.game))
            self.__matches.remove(existing_match)
            match = dataclasses.replace(existing_match, players=frozenset([*existing_match.players, websocket]))
            self.__matches.add(match)
            if not match.accepting_players(message.game):
                await self.broadcast(match)
        except StopIteration:
            match = Match.create(message, websocket)
            self.__matches.add(match)

    @staticmethod
    async def broadcast(match):
        [await websocket.send(MatchStartedMessage(position).to_payload().to_json()) for position, websocket in enumerate(match.players)]
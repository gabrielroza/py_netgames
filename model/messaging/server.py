import dataclasses
from typing import Type, Dict, Callable, TypeVar, Set

from websockets import WebSocketServerProtocol

from model.domain.game import Game
from model.domain.match import Match
from model.messaging.message import MatchStartMessage, Message

T = TypeVar('T', bound=Message)


class Server:
    __matches: Set[Match]
    __games: Set[Game]
    __handle_table: Dict[Type[T], Callable[[T, WebSocketServerProtocol], None]]

    def __init__(self):
        super().__init__()
        self.__games = set()
        self.__matches = set()
        self.__handle_table = {
            MatchStartMessage: self.start_match
        }

    def handle(self, message: Message, websocket: WebSocketServerProtocol):
        self.__handle_table[message.__class__](message, websocket)

    def start_match(self, message: MatchStartMessage, websocket: WebSocketServerProtocol):
        try:
            existing_match = next(
                match for match in self.__matches if match.accepting_players(message.game) and message)
            self.__matches.remove(existing_match)
            match = dataclasses.replace(existing_match, players=frozenset([*existing_match.players, websocket]))
            self.__matches.add(match)
        except StopIteration:
            match = Match.create(message, websocket)
            self.__matches.add(match)
        print(match)

from dataclasses import dataclass, field
from typing import FrozenSet

from websockets import WebSocketServerProtocol

from model.domain.game import Game
from model.messaging.message import MatchRequestMessage

__acc = 0


def _get_id():
    global __acc
    __acc += 1
    return __acc


@dataclass(eq=True, frozen=True)
class Match:
    game: Game
    id: int = field(default_factory=_get_id)
    amount_of_players: int = field(default_factory=2)
    players: FrozenSet[WebSocketServerProtocol] = field(default_factory=frozenset)

    @classmethod
    def create(cls, message: MatchRequestMessage, websocket: WebSocketServerProtocol):
        return Match(game=message.game, amount_of_players=message.amount_of_players, players=frozenset([websocket]))

    def accepting_players(self, game: Game) -> bool:
        return game == self.game and len(self.players) < self.amount_of_players

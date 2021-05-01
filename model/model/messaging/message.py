from abc import ABC
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from model.domain.game import Game


@dataclass
class Message(ABC):
    pass


@dataclass_json
@dataclass
class MatchStartMessage(Message):
    player_name: str
    game: Game
    amount_of_players: int

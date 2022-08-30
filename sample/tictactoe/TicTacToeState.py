import dataclasses


@dataclasses.dataclass
class TicTacToeState:
    game_over: bool
    description: str

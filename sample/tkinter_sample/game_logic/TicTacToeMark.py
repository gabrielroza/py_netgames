from enum import Enum


class TicTacToeMark(str, Enum):
    CROSS = 'X'
    CIRCLE = 'O'

    def opposite(self):
        return {
            TicTacToeMark.CROSS: TicTacToeMark.CIRCLE,
            TicTacToeMark.CIRCLE: TicTacToeMark.CROSS
        }[self]
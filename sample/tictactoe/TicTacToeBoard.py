import itertools
from typing import Optional, Tuple

from tictactoe.StalemateException import StalemateException
from tictactoe.TicTacToeMark import TicTacToeMark


class TicTacToeBoard:
    _board: [Optional[TicTacToeMark], Optional[TicTacToeMark]]

    def __init__(self) -> None:
        self._board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

        self.players = dict()
        super().__init__()

    def mark(self, mark: TicTacToeMark, coordinate: Tuple[int, int]) -> bool:
        if not self._board[coordinate[0]][coordinate[1]]:
            self._board[coordinate[0]][coordinate[1]] = mark
            return True
        else:
            return False

    def get_winner(self) -> Optional[TicTacToeMark]:
        winning_coordinates = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],

            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],

            [(0, 0), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (0, 2)],
        ]

        def get_winning_symbol(coordinates) -> Optional[TicTacToeMark]:
            values = (self._board[position[0]][position[1]] for position in coordinates)
            marks = [mark for mark in values if mark is not None]
            complete = len(marks) == 3 and len(set(marks)) == 1
            return self._board[coordinates[0][0]][coordinates[0][1]] if complete else None

        try:
            lane_winning_symbols = (get_winning_symbol(lane) for lane in winning_coordinates)
            return next(winning_symbol for winning_symbol in lane_winning_symbols if winning_symbol)
        except StopIteration:
            if None not in list(itertools.chain.from_iterable(self._board)):
                raise StalemateException()

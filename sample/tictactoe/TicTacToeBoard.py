import itertools
import json
from dataclasses import dataclass
from typing import Optional, Tuple, List, Literal, Dict

from tictactoe.StalemateException import StalemateException
from tictactoe.TicTacToeMark import TicTacToeMark

TicTacToeCoordinate = Tuple[Literal[0, 1, 2], Literal[0, 1, 2]]


@dataclass
class TicTacToeBoard:
    _board: List[List[Optional[TicTacToeMark]]]

    def __init__(self, board=None) -> None:
        self._board = board if board else [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        super().__init__()

    @classmethod
    def from_json(cls, value: str):
        return TicTacToeBoard(board=json.loads(value))

    def mark(self, mark: TicTacToeMark, coordinate: TicTacToeCoordinate) -> bool:
        if not self._board[coordinate[0]][coordinate[1]]:
            self._board[coordinate[0]][coordinate[1]] = mark
            return True
        else:
            return False

    def get_winner(self) -> Optional[TicTacToeMark]:
        winning_coordinates: List[List[TicTacToeCoordinate]] = [
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
            return marks[0] if complete else None

        try:
            lane_winning_symbols = (get_winning_symbol(lane) for lane in winning_coordinates)
            return next(winning_symbol for winning_symbol in lane_winning_symbols if winning_symbol)
        except StopIteration:
            if None not in list(itertools.chain.from_iterable(self._board)):
                raise StalemateException()

    def get_filled_coordinates(self) -> Dict[TicTacToeCoordinate, TicTacToeMark]:
        return {
            (row_index, column_index): value for row_index, row in enumerate(self._board) for column_index, value in enumerate(row) if value
        }

    def to_json(self) -> str:
        return json.dumps(self._board)

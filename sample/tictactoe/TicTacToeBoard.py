import itertools
from dataclasses import dataclass
from typing import Optional, Tuple, List, Literal, Dict

from tictactoe.StalemateException import StalemateException
from tictactoe.TicTacToeMark import TicTacToeMark
from tictactoe.TicTacToeState import TicTacToeState

TicTacToeCoordinate = Tuple[Literal[0, 1, 2], Literal[0, 1, 2]]


@dataclass
class TicTacToeBoard:
    _board: List[List[Optional[TicTacToeMark]]]
    _mark: TicTacToeMark
    _is_turn: bool

    def __init__(self, position: int=0, board=None) -> None:
        self._board = board if board else [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self._is_turn = position == 0
        self._mark = TicTacToeMark.CROSS if self._is_turn else TicTacToeMark.CIRCLE
        super().__init__()

    def mark(self, coordinate: TicTacToeCoordinate) -> bool:
        if self._is_turn and not self._board[coordinate[0]][coordinate[1]]:
            self._board[coordinate[0]][coordinate[1]] = self._mark
            self._is_turn = False
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

    def get_coordinates(self) -> Dict[TicTacToeCoordinate, Optional[TicTacToeMark]]:
        return {
            (row_index, column_index): value for row_index, row in enumerate(self._board) for column_index, value in
            enumerate(row)
        }

    def get_filled_coordinates(self) -> Dict[TicTacToeCoordinate, TicTacToeMark]:
        return {
            coordinate: value for coordinate, value in self.get_coordinates().items() if value
        }

    def flip(self):
        self._is_turn = not self._is_turn
        self._mark = {
            TicTacToeMark.CROSS: TicTacToeMark.CIRCLE,
            TicTacToeMark.CIRCLE: TicTacToeMark.CROSS
        }[self._mark]
        return self

    def get_state(self) -> TicTacToeState:
        game_over = False
        try:
            if not self._is_turn and self.get_winner():
                message = self.get_winner() + " won"
                game_over = True
            elif self._is_turn:
                message = "Make your move"
            else:
                message = "Awaiting opponent's move"
        except StalemateException:
            message = "Draw"
            game_over = True

        return TicTacToeState(game_over, message)

    def to_dict(self):
        return vars(self)

    @classmethod
    def from_dict(cls, attributes: Dict):
        board = TicTacToeBoard()
        board._board = attributes["_board"]
        board._is_turn = attributes["_is_turn"]
        board._mark = attributes["_mark"]
        return board


import unittest

from tictactoe.StalemateException import StalemateException
from tictactoe.TicTacToeBoard import TicTacToeBoard
from tictactoe.TicTacToeMark import TicTacToeMark


class TicTacToeTest(unittest.TestCase):

    def test_winning_scenarios(self):
        winning_board_configurations = [
            [
                [TicTacToeMark.CROSS, TicTacToeMark.CROSS, TicTacToeMark.CROSS],
                [None, None, None],
                [None, None, None]
            ],
            [
                [None, None, None],
                [TicTacToeMark.CROSS, TicTacToeMark.CROSS, TicTacToeMark.CROSS],
                [None, None, None]
            ],
            [
                [None, None, None],
                [None, None, None],
                [TicTacToeMark.CROSS, TicTacToeMark.CROSS, TicTacToeMark.CROSS],
            ],
            [
                [TicTacToeMark.CROSS, None, None],
                [TicTacToeMark.CROSS, None, None],
                [TicTacToeMark.CROSS, None, None],
            ],
            [
                [None, TicTacToeMark.CROSS, None],
                [None, TicTacToeMark.CROSS, None],
                [None, TicTacToeMark.CROSS, None],
            ],
            [
                [None, None, TicTacToeMark.CROSS],
                [None, None, TicTacToeMark.CROSS],
                [None, None, TicTacToeMark.CROSS],
            ],

            [
                [TicTacToeMark.CROSS, None, None],
                [None, TicTacToeMark.CROSS, None],
                [None, None, TicTacToeMark.CROSS],
            ],
            [
                [None, None, TicTacToeMark.CROSS],
                [None, TicTacToeMark.CROSS, None],
                [TicTacToeMark.CROSS, None, None],
            ]
        ]

        for winning_board_configuration in winning_board_configurations:
            self.assertEqual(TicTacToeMark.CROSS, TicTacToeBoard(winning_board_configuration).get_winner())

    def test_handles_different_marks(self):
        board_with_both_symbols = [
            [None, TicTacToeMark.CIRCLE, None],
            [TicTacToeMark.CROSS, TicTacToeMark.CROSS, TicTacToeMark.CROSS],
            [None, TicTacToeMark.CIRCLE, None]
        ]

        self.assertEqual(TicTacToeMark.CROSS,  TicTacToeBoard(board_with_both_symbols).get_winner())

    def test_handles_ordered_marking(self):
        board = TicTacToeBoard()
        self.assertIsNone(board.get_winner())
        board.mark(TicTacToeMark.CIRCLE, (0, 0))
        self.assertIsNone(board.get_winner())
        board.mark(TicTacToeMark.CROSS, (1, 0))
        self.assertIsNone(board.get_winner())
        board.mark(TicTacToeMark.CIRCLE, (0, 1))
        self.assertIsNone(board.get_winner())
        board.mark(TicTacToeMark.CROSS, (1, 1))
        self.assertIsNone(board.get_winner())
        board.mark(TicTacToeMark.CIRCLE, (0, 2))
        self.assertEqual(TicTacToeMark.CIRCLE, board.get_winner())

    def test_handles_mark_same_spot(self):
        board = TicTacToeBoard()
        self.assertTrue(board.mark(TicTacToeMark.CIRCLE, (0, 0)))
        self.assertFalse(board.mark(TicTacToeMark.CIRCLE, (0, 0)))

    def test_handles_stalemate(self):
        board_with_both_symbols = [
            [TicTacToeMark.CROSS, TicTacToeMark.CIRCLE, TicTacToeMark.CROSS],
            [TicTacToeMark.CROSS, TicTacToeMark.CROSS, TicTacToeMark.CIRCLE],
            [TicTacToeMark.CIRCLE, TicTacToeMark.CROSS, TicTacToeMark.CIRCLE]
        ]

        self.assertRaises(StalemateException, TicTacToeBoard(board_with_both_symbols).get_winner)

    def test_serializes_back_and_forth(self):
        board = [
            [TicTacToeMark.CROSS, TicTacToeMark.CROSS, TicTacToeMark.CIRCLE],
            [None, TicTacToeMark.CROSS, TicTacToeMark.CIRCLE],
            [None, TicTacToeMark.CIRCLE, TicTacToeMark.CROSS]
        ]

        self.assertEqual(TicTacToeBoard(board), TicTacToeBoard.from_json(TicTacToeBoard(board).to_json()))
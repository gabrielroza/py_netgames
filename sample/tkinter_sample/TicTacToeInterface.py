from tkinter import Tk, Button

from gameclient.pygameclient.PygameWebsocketProxy import PygameWebsocketProxy
from model.messaging.message import MatchStartedMessage, MoveMessage

from tictactoe.TicTacToeBoard import TicTacToeBoard, TicTacToeCoordinate
from tictactoe.TicTacToeMark import TicTacToeMark


class TicTacToeInterface:
    _board: TicTacToeBoard
    _websocket: PygameWebsocketProxy
    _is_turn: bool
    _mark: TicTacToeMark
    _is_running: bool
    _root: Tk

    def __init__(self, message: MatchStartedMessage, root: Tk, websocket: PygameWebsocketProxy) -> None:
        super().__init__()
        # self.match_id = message.match_id
        # self._is_turn = message.position == 0
        # self._mark = TicTacToeMark.CROSS if self._is_turn else TicTacToeMark.CIRCLE
        # self._websocket = websocket
        # self._board = TicTacToeBoard() if self._is_turn else None
        self._board = TicTacToeBoard([
            [TicTacToeMark.CROSS, TicTacToeMark.CROSS, TicTacToeMark.CIRCLE],
            [None, TicTacToeMark.CROSS, TicTacToeMark.CIRCLE],
            [None, TicTacToeMark.CIRCLE, TicTacToeMark.CROSS]
        ])
        # self._is_running = True
        self._root = root
        self._setup()
        root.mainloop()
        self._run()

    def _setup(self):
        self._root.title("Tic Tac Toe")
        self._root.resizable(0, 0)
        self._update_screen()

    def _update_screen(self):
        def build_button(coordinate: TicTacToeCoordinate, value: TicTacToeMark):
            button = Button(height=4, width=8, font=("Helvetica", "30"), command=lambda: self._handle_click(coordinate))
            button.grid(row=coordinate[0], column=coordinate[1])
            if value:
                button.configure(text=value)

        [build_button(coordinate, value) for coordinate, value in self._board.get_coordinates().items()]

    def _run(self):
        pass

    def _handle_click(self, coordinate: TicTacToeCoordinate):
        if self._is_turn and self._board.mark(self._mark, coordinate):
            self._is_turn = False
            self._websocket.send_move(self.match_id, self._board.to_json())
            self._update_screen()

    def _handle_move_received(self, message: MoveMessage):
        self._board = TicTacToeBoard.from_json(message.payload)
        self._is_turn = True
        self._update_screen()

from tkinter import Tk, Button
from uuid import UUID

from gameclient.tkinterclient.TkinterWebsocketProxy import TkinterWebsocketProxy
from model.messaging.message import MatchStartedMessage, MoveMessage

from tictactoe.TicTacToeBoard import TicTacToeBoard, TicTacToeCoordinate
from tictactoe.TicTacToeMark import TicTacToeMark
from tkinter_sample import WINDOW_WIDTH, WINDOW_HEIGHT
from tkinter_sample.ServerConnectionMenubar import ServerConnectionMenubar


class TicTacToeInterface:
    _tk: Tk
    _websocket: TkinterWebsocketProxy
    _game_id: UUID

    _board: TicTacToeBoard
    _is_turn: bool
    _mark: TicTacToeMark

    def __init__(self) -> None:
        super().__init__()

        def _setup_tk() -> Tk:
            tk = Tk()
            tk.title("Tic Tac Toe")
            tk.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
            return tk

        self._tk = _setup_tk()
        self._websocket = TkinterWebsocketProxy()
        self._game_id = UUID('b6625465-9478-4331-9e68-ffac2f02942f')
        self.menu_bar = ServerConnectionMenubar(self._websocket, self._tk)

        self._board = TicTacToeBoard()
        self._is_turn = False
        self._mark = TicTacToeMark.CROSS

    def _update_screen(self):
        def build_button(coordinate: TicTacToeCoordinate, value: TicTacToeMark):
            button = Button(height=4, width=8, font=("Helvetica", "30"), command=lambda: self._handle_click(coordinate))
            button.grid(row=coordinate[0], column=coordinate[1])
            if value:
                button.configure(text=value)

        [build_button(coordinate, value) for coordinate, value in self._board.get_coordinates().items()]

    def run(self):
        self._tk.config(menu=self.menu_bar)
        self._update_screen()
        self._websocket.add_listener(self)
        self._tk.mainloop()

    def _handle_click(self, coordinate: TicTacToeCoordinate):
        print(coordinate)
        if self._is_turn and self._board.mark(self._mark, coordinate):
            self._is_turn = False
            self._websocket.send_move(self.match_id, self._board.to_json())
            self._update_screen()

    def match_started(self, match: MatchStartedMessage):
        print(match)

    def receive_move(self, message: MoveMessage):
        print(message)
        # self._board = TicTacToeBoard.from_json(message.payload)
        # self._is_turn = True
        # self._update_screen()

    def receive_disconnect(self):
        print("Disconnected")
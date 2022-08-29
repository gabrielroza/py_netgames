from tkinter import Tk, Button
from uuid import UUID

from gameclient.tkinterclient.TkinterWebsocketListener import TkinterWebsocketListener
from gameclient.tkinterclient.TkinterWebsocketProxy import TkinterWebsocketProxy
from model.messaging.message import MatchStartedMessage, MoveMessage

from tictactoe.TicTacToeBoard import TicTacToeBoard, TicTacToeCoordinate
from tictactoe.TicTacToeMark import TicTacToeMark
from tkinter_sample import WINDOW_WIDTH, WINDOW_HEIGHT
from tkinter_sample.ServerConnectionMenubar import ServerConnectionMenubar


class TicTacToeInterface(TkinterWebsocketListener):
    _tk: Tk
    _websocket: TkinterWebsocketProxy
    _game_id: UUID
    _menu_bar = ServerConnectionMenubar
    _ongoing_match: bool
    _match_id: UUID
    _is_turn: bool
    _mark: TicTacToeMark
    _board: TicTacToeBoard

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
        self._menu_bar = ServerConnectionMenubar(self._websocket, self._tk)
        self.ongoing_match = False
        self.match_id = None
        self._is_turn = False
        self._mark = None
        self._board = None

    def _update_screen(self):
        def build_button(coordinate: TicTacToeCoordinate, value: TicTacToeMark):
            button = Button(height=4, width=8, font=("Helvetica", "30"), command=lambda: self._handle_click(coordinate))
            button.grid(row=coordinate[0], column=coordinate[1])
            if value:
                button.configure(text=value)

        if self.ongoing_match:
            [build_button(coordinate, value) for coordinate, value in self._board.get_coordinates().items()]

    def run(self):
        self._tk.config(menu=self._menu_bar)
        self._update_screen()
        self._websocket.add_listener(self)
        self._tk.mainloop()

    def _handle_click(self, coordinate: TicTacToeCoordinate):
        print(coordinate)
        if self.ongoing_match and self._is_turn and self._board.mark(self._mark, coordinate):
            self._is_turn = False
            self._websocket.send_move(self.match_id, self._board.to_json())
            self._update_screen()

    def match_started(self, message: MatchStartedMessage):
        self.ongoing_match = True
        self.match_id = message.match_id
        self._is_turn = message.position == 0
        self._mark = TicTacToeMark.CROSS if self._is_turn else TicTacToeMark.CIRCLE
        self._board = TicTacToeBoard() if self._is_turn else None
        self._update_screen()

    def receive_move(self, message: MoveMessage):
        print(message)
        self._board = TicTacToeBoard.from_json(message.payload)
        self._is_turn = True
        self._update_screen()

    def receive_disconnect(self):
        print("Disconnected")

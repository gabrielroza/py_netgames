import logging
from tkinter import Tk, Button, Label, CENTER
from typing import Dict
from uuid import UUID

from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener
from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_model.messaging.message import MatchStartedMessage, MoveMessage

from tictactoe.TicTacToeBoard import TicTacToeBoard, TicTacToeCoordinate
from tictactoe.TicTacToeMark import TicTacToeMark
from tkinter_sample import WINDOW_WIDTH, WINDOW_HEIGHT
from tkinter_sample.ServerConnectionMenubar import ServerConnectionMenubar


class TicTacToeInterface(PyNetgamesServerListener):
    _tk: Tk
    _server_proxy: PyNetgamesServerProxy
    _menu_bar = ServerConnectionMenubar
    _ongoing_match: bool
    _match_id: UUID
    _board: TicTacToeBoard
    _buttons: Dict[TicTacToeCoordinate, Button]

    def __init__(self) -> None:
        super().__init__()

        def _setup_tk() -> Tk:
            tk = Tk()
            tk.title("Tic Tac Toe")
            tk.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
            return tk

        self._tk = _setup_tk()
        self._server_proxy = PyNetgamesServerProxy()
        self._menu_bar = ServerConnectionMenubar(self._server_proxy, self._tk)
        self._ongoing_match = False
        self.match_id = None
        self._board = None
        self._buttons = {}
        self._label = None

    def _update_screen(self):
        def build_button(coordinate: TicTacToeCoordinate, value: TicTacToeMark = None) -> Button:
            button = Button(height=4, width=8, font=("Helvetica", "30"), command=lambda: self._handle_click(coordinate))
            button.grid(row=coordinate[0], column=coordinate[1])
            self._buttons[coordinate] = button
            if value:
                button.configure(text=value)
            return button

        if self._ongoing_match:
            state = self._board.get_state()
            [self._buttons[coordinate].configure(text=value) for coordinate, value in
             self._board.get_filled_coordinates().items()]
            self._label.configure(text=state.description)

            if state.game_over:
                self._board = None
                self._ongoing_match = False
                self._tk.after(3000, self._menu_bar.disconnect)

        else:
            [button.destroy() for button in self._buttons.values()]
            self._buttons = {}
            if self._label:
                self._label.destroy()
                self._label = None
            self._buttons = {coordinate: build_button(coordinate) for coordinate in
                             TicTacToeBoard.get_coordinates()}
            self._label = Label(self._tk, text="Awaiting match", anchor=CENTER)
            self._label.grid(row=3, column=1)

    def run(self):
        self._tk.config(menu=self._menu_bar)
        self._update_screen()
        self._server_proxy.add_listener(self)
        self._tk.mainloop()

    def _handle_click(self, coordinate: TicTacToeCoordinate):
        print(coordinate)
        if self._ongoing_match and self._board.mark(coordinate):
            self._server_proxy.send_move(self.match_id, self._board.to_dict())
            self._update_screen()

    def receive_connection_success(self):
        self._menu_bar.connection_confirmed()

    def receive_match(self, message: MatchStartedMessage):
        self._ongoing_match = True
        self.match_id = message.match_id
        self._board = TicTacToeBoard(position=message.position)
        self._update_screen()

    def receive_move(self, message: MoveMessage):
        self._board = TicTacToeBoard.from_dict(message.payload).flip()
        self._update_screen()

    def receive_error(self, error):
        self._menu_bar.connection_error(error)
        self._ongoing_match = False
        self._update_screen()

    def receive_disconnect(self):
        self._menu_bar.disconnect()
        self._ongoing_match = False
        self._update_screen()


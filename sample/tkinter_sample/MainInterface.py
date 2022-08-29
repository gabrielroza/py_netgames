from tkinter import Tk, Entry, Menu
from tkinter import simpledialog
from uuid import UUID

from gameclient.tkinterclient.TkinterWebsocketProxy import TkinterWebsocketProxy

from tkinter_sample import WINDOW_WIDTH, WINDOW_HEIGHT
from tkinter_sample.ServerConnectionMenubar import ServerConnectionMenubar


class MainInterface:
    _root: Tk
    _websocket: TkinterWebsocketProxy
    _game_id: UUID

    def __init__(self) -> None:
        super().__init__()
        self._websocket = TkinterWebsocketProxy()
        self._game_id = UUID('b6625465-9478-4331-9e68-ffac2f02942f')
        self._root = self._setup_tk()
        self.menu_bar = ServerConnectionMenubar(self._websocket, self._root)

    def run(self):
        self.menu_bar.configure()
        self._root.mainloop()

    def _setup_tk(self) -> Tk:
        tk = Tk()
        tk.title("Tic Tac Toe")
        tk.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        return tk

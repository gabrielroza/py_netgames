from tkinter import Tk, Entry, Menu
from tkinter import simpledialog
from uuid import UUID

from gameclient.tkinterclient.TkinterWebsocketProxy import TkinterWebsocketProxy

from tkinter_sample import WINDOW_WIDTH, WINDOW_HEIGHT


class MainInterface:
    _is_running: bool
    _root: Tk
    _websocket: TkinterWebsocketProxy
    _game_id: UUID
    _address_field: Entry

    def __init__(self) -> None:
        super().__init__()
        self._websocket = TkinterWebsocketProxy()
        self._game_id = UUID('b6625465-9478-4331-9e68-ffac2f02942f')
        self._root = self._setup_tk()
        self._menu_bar = self._build_menu_bar()

    def run(self):
        self._root.mainloop()

    def _setup_tk(self) -> Tk:
        tk = Tk()
        tk.title("Tic Tac Toe")
        tk.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        return tk

    def _connect(self):
        user_input = simpledialog.askstring("Server address", "Server address", initialvalue="localhost:8765")
        self._websocket.connect(user_input)
        self._menu_bar.entryconfig("Disconnect", state="normal")
        self._menu_bar.entryconfig("Connect", state="disabled")

    def _disconnect(self):
        self._websocket.disconnect()
        self._menu_bar.entryconfig("Disconnect", state="disabled")
        self._menu_bar.entryconfig("Connect", state="normal")

    def _build_menu_bar(self):
        menubar = Menu(self._root)
        connect = Menu(menubar, tearoff=0)
        connect.add_command(label="Connect", command=self._connect)
        connect.add_command(label="Disconnect", command=self._disconnect, state='disabled')
        connect.add_separator()
        connect.add_command(label="Exit", command=self._root.quit)
        menubar.add_cascade(label="Connection", menu=connect)
        self._root.config(menu=menubar)
        return connect

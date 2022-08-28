from tkinter import Tk, Entry, Menu
from tkinter import simpledialog
from uuid import UUID

from gameclient.tkinterclient.TkinterWebsocketProxy import TkinterWebsocketProxy

from tkinter_sample import WINDOW_WIDTH, WINDOW_HEIGHT


class MainInterface:
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
        self._connect_dropdown = self._build_connect_dropdown()
        self._match_dropdown = self._build_match_dropdown()

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
        self._connect_dropdown.entryconfig("Disconnect", state="normal")
        self._connect_dropdown.entryconfig("Connect", state="disabled")
        self._match_dropdown.entryconfig("Request Match", state="normal")

    def _disconnect(self):
        self._websocket.disconnect()
        self._connect_dropdown.entryconfig("Disconnect", state="disabled")
        self._connect_dropdown.entryconfig("Connect", state="normal")
        self._match_dropdown.entryconfig("Request Match", state="disabled")

    def _request_match(self):
        pass

    def _build_connect_dropdown(self):
        connect = Menu(self._menu_bar, tearoff=0)
        connect.add_command(label="Connect", command=self._connect)
        connect.add_command(label="Disconnect", command=self._disconnect, state='disabled')
        connect.add_separator()
        connect.add_command(label="Exit", command=self._root.quit)
        self._menu_bar.add_cascade(label="Connection", menu=connect)
        return connect

    def _build_match_dropdown(self):
        match = Menu(self._menu_bar, tearoff=0)
        match.add_command(label="Request Match", command=self._request_match, state='disabled')
        self._menu_bar.add_cascade(label="Match", menu=match)
        return match

    def _build_menu_bar(self):
        bar = Menu(self._root)
        self._root.config(menu=bar)
        return bar

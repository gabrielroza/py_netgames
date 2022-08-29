from tkinter import Tk, Menu
from tkinter import simpledialog
from uuid import UUID

from gameclient.tkinterclient.TkinterWebsocketProxy import TkinterWebsocketProxy


class ServerConnectionMenubar:

    def __init__(self, websocket: TkinterWebsocketProxy, tk: Tk) -> None:
        super().__init__()
        self._websocket = websocket
        self._game_id = UUID('b6625465-9478-4331-9e68-ffac2f02942f')
        self._tk = tk
        self._menu_bar = self._build_menu_bar()
        self._connect_dropdown = self._build_connect_dropdown()
        self._match_dropdown = self._build_match_dropdown()

    def configure(self):
        self._tk.config(menu=self._menu_bar)

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
        self._websocket.request_match(self._game_id, amount_of_players=2)

    def _build_connect_dropdown(self):
        connect = Menu(self._menu_bar, tearoff=0)
        connect.add_command(label="Connect", command=self._connect)
        connect.add_command(label="Disconnect", command=self._disconnect, state='disabled')
        connect.add_separator()
        connect.add_command(label="Exit", command=self._tk.quit)
        self._menu_bar.add_cascade(label="Connection", menu=connect)
        return connect

    def _build_match_dropdown(self):
        match = Menu(self._menu_bar, tearoff=0)
        match.add_command(label="Request Match", command=self._request_match, state='disabled')
        self._menu_bar.add_cascade(label="Match", menu=match)
        return match

    def _build_menu_bar(self):
        return Menu(self._tk)
import os
from tkinter import Tk, Menu
from tkinter import simpledialog

from py_netgames_client.tkinter_client.TkinterWebsocketProxy import TkinterWebsocketProxy


class ServerConnectionMenubar(Menu):
    _tk: Tk
    _websocket: TkinterWebsocketProxy
    _connect_dropdown: Menu
    _match_dropdown: Menu

    def __init__(self, websocket: TkinterWebsocketProxy, tk: Tk, **kwargs) -> None:
        super().__init__(tk, **kwargs)
        self._tk = tk
        self._websocket = websocket
        self._connect_dropdown = self._build_connect_dropdown()
        self._match_dropdown = self._build_match_dropdown()

    def _connect(self):
        user_input = simpledialog.askstring("Server address", "Server address", initialvalue="localhost:8765")
        self._websocket.send_connect(user_input)
        self._connect_dropdown.entryconfig("Disconnect", state="disabled")
        self._connect_dropdown.entryconfig("Connect", state="disabled")
        self._match_dropdown.entryconfig("Request Match", state="disabled")

    def disconnect(self):
        self._websocket.send_disconnect()
        self._connect_dropdown.entryconfig("Disconnect", state="disabled")
        self._connect_dropdown.entryconfig("Connect", state="normal")
        self._match_dropdown.entryconfig("Request Match", state="disabled")

    def connection_confirmed(self):
        self._connect_dropdown.entryconfig("Disconnect", state="normal")
        self._connect_dropdown.entryconfig("Connect", state="disabled")
        self._match_dropdown.entryconfig("Request Match", state="normal")

    def connection_error(self, error: Exception):
        self._connect_dropdown.entryconfig("Disconnect", state="disabled")
        self._connect_dropdown.entryconfig("Connect", state="normal")
        self._match_dropdown.entryconfig("Request Match", state="disabled")

    def _request_match(self):
        self._websocket.send_match(amount_of_players=2)

    def _build_connect_dropdown(self):
        connect = Menu(self, tearoff=0)
        connect.add_command(label="Connect", command=self._connect)
        connect.add_command(label="Disconnect", command=self.disconnect, state='disabled')
        connect.add_separator()
        connect.add_command(label="Exit", command=lambda: os._exit(0))
        self.add_cascade(label="Connection", menu=connect)
        return connect

    def _build_match_dropdown(self):
        match = Menu(self, tearoff=0)
        match.add_command(label="Request Match", command=self._request_match, state='disabled')
        self.add_cascade(label="Match", menu=match)
        return match

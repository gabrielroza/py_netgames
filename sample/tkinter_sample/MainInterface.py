from tkinter import Tk, Label, Entry, Frame, CENTER, Widget, Button, DISABLED
from uuid import UUID

from gameclient.tkinterclient.TkinterWebsocketProxy import TkinterWebsocketProxy

from tkinter_sample import WINDOW_WIDTH, WINDOW_HEIGHT


class MainInterface:
    _is_running: bool
    _root: Widget
    _websocket: TkinterWebsocketProxy
    _game_id: UUID
    _address_field: Entry

    def __init__(self) -> None:
        super().__init__()
        self._websocket = TkinterWebsocketProxy()
        self._game_id = UUID('b6625465-9478-4331-9e68-ffac2f02942f')
        self._root = self._setup_tk()
        self._address_field = self._build_server_address_field()
        self._connect_button = self._build_connect_button()
        self._build_match_request_button()
        self._build_quit_button()

    def run(self):
        self._root.mainloop()

    def _setup_tk(self) -> Widget:
        tk = Tk()
        tk.title("Tic Tac Toe")
        tk.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        frame = Frame(tk)
        frame.place(relx=.5, rely=.5, anchor=CENTER)
        return frame

    def _build_server_address_field(self) -> Entry:
        Label(self._root, text='Server address: ').grid(row=0)
        address_entry: Entry = Entry(self._root)
        address_entry.insert(0, 'localhost:8765')
        address_entry.grid(row=0, column=1)
        return address_entry

    def _build_connect_button(self) -> Button:
        Label(self._root, text='Connection Status: ').grid(row=1)

        def _handle_connect_click():
            if self._connect_button["text"] == "Disconnected":
                self._websocket.connect(self._address_field.get())
                self._connect_button["text"] = "Connected"

        button = Button(self._root, text="Disconnected", command=_handle_connect_click, relief="groove")
        # button["state"] = DISABLED
        button.grid(row=1, column=1)
        return button

    def _build_match_request_button(self):
        Label(self._root, text='Request Match: ').grid(row=2)

        def _handle_request_click():
            pass

        button = Button(self._root, text="Request", command=_handle_request_click, relief="groove")
        button["state"] = DISABLED
        button.grid(row=2, column=1)
        return button

    def _build_quit_button(self):
        pass

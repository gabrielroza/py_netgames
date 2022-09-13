from typing import List

from py_netgames_model.messaging.message import MatchStartedMessage, MoveMessage

from py_netgames_client._base.BaseWebsocketProxy import BaseWebsocketProxy
from py_netgames_client.tkinter_client.TkinterWebsocketListener import TkinterWebsocketListener


class TkinterWebsocketProxy(BaseWebsocketProxy):
    _listeners: List[TkinterWebsocketListener]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._listeners = []

    def add_listener(self, listener: TkinterWebsocketListener):
        self._listeners.append(listener)

    def _receive_match_start(self, match: MatchStartedMessage):
        [listener.receive_match(match) for listener in self._listeners]

    def _receive_move(self, move: MoveMessage):
        [listener.receive_move(move) for listener in self._listeners]

    def _disconnection(self):
        [listener.receive_disconnect() for listener in self._listeners]

    def _connection_success(self):
        [listener.receive_connection_success() for listener in self._listeners]

    def _error(self, error: Exception):
        [listener.receive_error(error) for listener in self._listeners]

    def _match_requested_success(self):
        [listener.receive_match_requested_success() for listener in self._listeners]

    def _move_sent_success(self):
        [listener.receive_move_sent_success() for listener in self._listeners]

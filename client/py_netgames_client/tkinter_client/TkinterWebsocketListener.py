from abc import ABC

from py_netgames_model.messaging.message import MatchStartedMessage, MoveMessage


class TkinterWebsocketListener(ABC):

    def __init__(self) -> None:
        super().__init__()

    def receive_match(self, match: MatchStartedMessage):
        raise NotImplementedError("Method match_started not overwritten")

    def receive_move(self, match: MoveMessage):
        raise NotImplementedError("Method receive_move not overwritten")

    def receive_disconnect(self):
        raise NotImplementedError("Method receive_disconnect not overwritten")

    def receive_connection_success(self):
        pass

    def receive_error(self, error: Exception):
        pass

    def receive_match_requested_success(self):
        pass

    def receive_move_sent_success(self):
        pass

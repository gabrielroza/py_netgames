from abc import ABC

from model.messaging.message import MatchStartedMessage, MoveMessage


class TkinterWebsocketListener(ABC):

    def __init__(self) -> None:
        super().__init__()

    def match_started(self, match: MatchStartedMessage):
        raise NotImplementedError("Method match_started not overwritten")

    def receive_move(self, match: MoveMessage):
        raise NotImplementedError("Method receive_move not overwritten")

    def receive_disconnect(self):
        raise NotImplementedError("Method receive_disconnect not overwritten")

    def connection_success(self):
        pass

    def error(self, error: Exception):
        pass

    def match_requested_success(self):
        pass

    def move_sent_success(self):
        pass

from abc import ABC


class Listener(ABC):

    def match_started(self, position: int):
        raise NotImplementedError()

    def receive_move(self, payload: any):
        raise NotImplementedError()

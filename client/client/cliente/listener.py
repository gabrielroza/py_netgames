import abc
from abc import ABC


class Listener(ABC):

    @abc.abstractmethod
    def receive_move(self, payload: any):
        raise NotImplementedError()

import asyncio
import uuid

from client.cliente.listener import Listener
from client.cliente.proxy import Proxy


class Actor(Listener):

    def match_started(self, position: int):
        print('match started')

    def receive_move(self, payload: any):
        print('move received: ' + payload)


if __name__ == '__main__':
    game_id = uuid.uuid4()
    print(game_id)
    proxy = Proxy(Actor())
    proxy.connect("localhost:8765")
    proxy.request_match("gabriel", game_id, 2)
    proxy.request_match("gabriel", game_id, 2)

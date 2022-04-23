from uuid import UUID

import rel as rel
import websocket
from model.messaging.message import MatchRequestMessage
from websocket import WebSocketApp

from client.cliente.listener import Listener


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")


class Proxy:
    __listener: Listener
    __websocket: WebSocketApp

    def __init__(self, listener: Listener) -> None:
        super().__init__()
        self.__listener = listener

    def connect(self, address: str):
        self.__websocket = websocket.WebSocketApp(f"ws://{address}",
                                                  on_open=on_open,
                                                  on_message=on_message,
                                                  on_error=on_error,
                                                  on_close=on_close)
        self.__websocket.run_forever(dispatcher=rel)
        rel.signal(2, rel.abort)
        rel.dispatch()

    def request_match(self, player_name: str, game_id: UUID, amount_of_players: int):
        payload = MatchRequestMessage(player_name, game_id, amount_of_players).to_payload().to_json()
        print(payload)
        self.__websocket.send(payload)

    def send_move(self, payload: any):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()

    def end_match(self):
        raise NotImplementedError()

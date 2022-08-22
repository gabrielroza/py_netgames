from uuid import UUID

from model.messaging.deserializer import WebhookPayloadDeserializer
from websockets.legacy.client import WebSocketClientProtocol


class TkinterWebsocketProxy:
    _websocket: WebSocketClientProtocol
    _deserializer: WebhookPayloadDeserializer

    def __init__(self) -> None:
        super().__init__()
        self.__deserializer = WebhookPayloadDeserializer()

    def connect(self, address: str) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def request_match(self, game_id: UUID, amount_of_players: int):
        pass

    def send_move(self, match_id: UUID, payload: str) -> None:
        pass

    def listen(self) -> None:
        pass

import websockets
from asgiref.sync import async_to_sync
from model.messaging.message import MatchRequestMessage
from websockets import WebSocketServerProtocol

from client.cliente.listener import Listener


class Proxy:
    __websocket: WebSocketServerProtocol
    __listeners: [Listener]

    def __init__(self, listeners: [Listener]) -> None:
        super().__init__()
        self.__listeners = listeners

    @async_to_sync
    async def connect(self, address: str):
        print("connecting...")
        self.__websocket = await websockets.connect("ws://" + address)

    @async_to_sync
    async def request_match(self, payload: MatchRequestMessage):
        await self.__websocket.send(payload)

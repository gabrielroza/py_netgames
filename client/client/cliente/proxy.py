import websockets
from asgiref.sync import async_to_sync
from websockets import WebSocketServerProtocol

from client.cliente.listener import Listener


class Proxy:
    __websocket: WebSocketServerProtocol
    __listeners: [Listener]

    def __init__(self, listeners: [Listener]) -> None:
        super().__init__()
        print("eae")
        self.__listeners = listeners

    @async_to_sync
    async def connect(self, address: str):
        async with websockets.connect("ws://" + address) as websocket:
            self.__websocket = websocket

    @async_to_sync
    async def send(self, payload: any):
        await self.__websocket.send(payload)

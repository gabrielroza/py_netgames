import asyncio

import websockets
from websockets import WebSocketServerProtocol

from model.messaging.deserializer import WebhookPayloadDeserializer
from server import Server


class MainLoop:
    __deserializer: WebhookPayloadDeserializer
    __server: Server

    def __init__(self) -> None:
        super().__init__()
        self.__deserializer = WebhookPayloadDeserializer()
        self.__server = Server()
        game_server = websockets.serve(self.listen, "localhost", 8765)
        print("Listening...")
        asyncio.get_event_loop().run_until_complete(game_server)
        asyncio.get_event_loop().run_forever()

    async def listen(self, websocket: WebSocketServerProtocol, path: str):
        async for message in websocket:
            self.__server.handle(self.__deserializer.deserialize(message), websocket)

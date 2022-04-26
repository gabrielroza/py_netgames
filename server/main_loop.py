import asyncio
import logging

import websockets
from model.messaging.deserializer import WebhookPayloadDeserializer
from websockets import WebSocketServerProtocol, ConnectionClosedError

from server import Server


class MainLoop:
    __deserializer: WebhookPayloadDeserializer
    __server: Server
    __logger: logging.Logger

    def __init__(self) -> None:
        super().__init__()
        port = 8765
        self.__deserializer = WebhookPayloadDeserializer()
        self.__server = Server()
        self.__logger = logging.getLogger("server.MainLoop")
        game_server = websockets.serve(self.listen, "localhost", port)
        asyncio.get_event_loop().run_until_complete(game_server)
        self.__logger.info(f"Server listening at port {port}")
        asyncio.get_event_loop().run_forever()

    async def listen(self, websocket: WebSocketServerProtocol, _: str):
        try:
            async for message in websocket:
                self.__logger.info(f"Message received: {message}")
                await self.__server.handle_message(self.__deserializer.deserialize(message), websocket)
        except ConnectionClosedError:
            await self.__server.handle_disconnect(websocket)
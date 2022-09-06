import asyncio
import logging

import websockets
from py_netgames_model.messaging.deserializer import WebhookPayloadDeserializer
from websockets import WebSocketServerProtocol, ConnectionClosedError

from server import Server


class MainLoop:
    _deserializer: WebhookPayloadDeserializer
    _server: Server
    _logger: logging.Logger

    def __init__(self) -> None:
        super().__init__()
        port = 8765
        self._deserializer = WebhookPayloadDeserializer()
        self._server = Server()
        self._logger = logging.getLogger("server.MainLoop")
        game_server = websockets.serve(self.listen, "localhost", port)
        asyncio.get_event_loop().run_until_complete(game_server)
        self._logger.info(f"Server listening at port {port}")
        asyncio.get_event_loop().run_forever()

    async def listen(self, websocket: WebSocketServerProtocol, _: str):
        try:
            async for message in websocket:
                self._logger.info(f"Message received: {message}")
                await self._server.handle_message(self._deserializer.deserialize(message), websocket)
            await self._server.handle_disconnect(websocket)
        except ConnectionClosedError as error:
            self._logger.error(f'ConnectionClosedError when listening: {error}')
            await self._server.handle_disconnect(websocket)
import asyncio
import logging

import websockets
from py_netgames_model.messaging.deserializer import WebhookPayloadDeserializer
from websockets import WebSocketServerProtocol, ConnectionClosedError
from websockets.legacy.server import WebSocketServer

from py_netgames_server.game_server import GameServer


class WebSocketServerBuilder:
    _deserializer: WebhookPayloadDeserializer
    _server: GameServer
    _logger: logging.Logger

    def __init__(self) -> None:
        super().__init__()
        self._deserializer = WebhookPayloadDeserializer()
        self._server = GameServer()
        self._logger = logging.getLogger("server.MainLoop")

    async def async_serve(self, port=8765) -> WebSocketServer:
        return await websockets.serve(self.listen, "localhost", port)

    def serve(self, port=8765):
        asyncio.get_event_loop().run_until_complete(websockets.serve(self.listen, "localhost", port))
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
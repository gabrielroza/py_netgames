import asyncio
import signal

import websockets
from py_netgames_model.messaging.deserializer import WebhookPayloadDeserializer
from websockets import WebSocketServerProtocol, ConnectionClosedError
from websockets.legacy.server import WebSocketServer

from py_netgames_server.game_server import GameServer


class WebSocketServerBuilder:
    _deserializer: WebhookPayloadDeserializer
    _server: GameServer

    def __init__(self) -> None:
        super().__init__()
        self._deserializer = WebhookPayloadDeserializer()
        self._server = GameServer()

    async def async_serve(self, host="0.0.0.0", port=8765) -> WebSocketServer:
        return await websockets.serve(self.listen, host, port)

    def serve(self, host, port, health_check):
        stop = asyncio.get_event_loop().create_future()
        asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, stop.set_result, None)
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self.listen, host, port, process_request=health_check))
        asyncio.get_event_loop().run_until_complete(stop)

    async def listen(self, websocket: WebSocketServerProtocol):
        try:
            async for message in websocket:
                await self._server.handle_message(self._deserializer.deserialize(message), websocket)
            await self._server.handle_disconnect(websocket)
        except ConnectionClosedError:
            await self._server.handle_disconnect(websocket)

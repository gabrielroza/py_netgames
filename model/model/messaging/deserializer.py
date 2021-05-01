from typing import Dict, Callable, Any

from model.messaging.message import Message, MatchStartMessage
from model.messaging.webhook_payload import WebhookPayload, WebhookPayloadType


class WebhookPayloadDeserializer:
    __deserialization_table: Dict[WebhookPayloadType, Callable[[Dict[str, Any]], Message]]

    def __init__(self):
        self.__deserialization_table = {
            WebhookPayloadType.MATCH_START: MatchStartMessage.from_dict
        }

    def deserialize(self, message) -> Message:
        webhook_payload = WebhookPayload.from_json(message)
        return self.__deserialization_table[webhook_payload.type](webhook_payload.message)

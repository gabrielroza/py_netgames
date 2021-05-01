import abc
from abc import ABC
from dataclasses import dataclass
from typing import Dict, Any
from uuid import UUID

from dataclasses_json import dataclass_json

from model.domain.game import Game
from model.messaging.webhook_payload import WebhookPayloadType, WebhookPayload


@dataclass
class Message(ABC):

    @abc.abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def type(self) -> WebhookPayloadType:
        pass

    def to_payload(self) -> WebhookPayload:
        return WebhookPayload(self.type(), self.to_dict())


@dataclass_json
@dataclass
class MatchRequestMessage(Message):
    player_name: str
    game: Game
    amount_of_players: int

    def type(self) -> WebhookPayloadType:
        return WebhookPayloadType.MATCH_REQUEST

    def to_dict(self) -> str:
        return MatchRequestMessage.to_dict(self)


@dataclass_json
@dataclass
class MatchStartedMessage(Message):
    match_id: UUID
    position: int

    def type(self) -> WebhookPayloadType:
        return WebhookPayloadType.MATCH_STARTED

    def to_dict(self) -> str:
        return MatchStartedMessage.to_dict(self)


@dataclass_json
@dataclass
class MoveMessage(Message):
    match_id: UUID
    payload: any

    def type(self) -> WebhookPayloadType:
        return WebhookPayloadType.MOVE

    def to_dict(self) -> str:
        return MoveMessage.to_dict(self)

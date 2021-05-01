from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

from dataclasses_json import dataclass_json


class WebhookPayloadType(Enum):
    MATCH_START = 'MATCH_START'


@dataclass_json
@dataclass
class WebhookPayload:
    type: WebhookPayloadType
    message: Dict[str, Any]

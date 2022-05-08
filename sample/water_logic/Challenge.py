from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from water_logic.ChallengeState import ChallengeState
from water_logic.Jar import Jar


@dataclass_json
@dataclass
class Challenge:
    left_jar: Jar
    right_jar: Jar
    maximum_steps: int
    description: str
    used_steps: int = field(default=0)
    state: ChallengeState = field(default=ChallengeState.IN_PROGRESS)

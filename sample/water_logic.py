from dataclasses import dataclass, field
from enum import Enum

from dataclasses_json import dataclass_json


class ChallengeState(Enum):
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    IN_PROGRESS = 'IN_PROGRESS'


@dataclass_json
@dataclass
class Jar:
    capacity: int
    goal: int
    fill: int = field(default=2)

    def goal_is_met(self):
        return self.fill == self.goal

    def is_full(self):
        return self.fill == self.capacity

    def is_empty(self):
        return self.fill == 0


@dataclass_json
@dataclass
class Challenge:
    left_jar: Jar
    right_jar: Jar
    maximum_steps: int
    description: str
    used_steps: int = field(default=0)
    state: ChallengeState = field(default=ChallengeState.IN_PROGRESS)

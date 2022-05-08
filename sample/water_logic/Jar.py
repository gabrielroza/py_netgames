from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Jar:
    capacity: int
    goal: Optional[int]
    fill: int = field(default=0)

    def goal_is_met(self) -> bool:
        return self.goal is None or self.fill == self.goal

    def is_full(self) -> bool:
        return self.fill == self.capacity

    def is_empty(self) -> bool:
        return self.fill == 0

    def empty(self) -> bool:
        if self.is_empty():
            return False
        self.fill = 0
        return True

    def fulfill(self) -> bool:
        if self.is_full():
            return False
        self.fill = self.capacity
        return True

    def transfer_to(self, destination: 'Jar') -> bool:
        if self.is_empty() or destination.is_full():
            return False

        fulfill_amount = destination.capacity - destination.fill

        if self.fill > fulfill_amount:
            destination.fill = destination.capacity
            self.fill = self.fill - fulfill_amount
        else:
            destination.fill = destination.fill + self.fill
            self.fill = 0
        return True

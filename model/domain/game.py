from dataclasses import dataclass
from uuid import UUID


@dataclass(eq=True, frozen=True)
class Game:
    id: UUID

import uuid
from pathlib import Path
from uuid import UUID


class IdentifierFileGenerator:

    def get_or_create_identifier(self) -> UUID:
        path = Path("gameid.txt")
        if path.is_file():
            return UUID(path.read_text())
        else:
            game_id = uuid.uuid4()
            path.write_text(str(game_id))
            return game_id

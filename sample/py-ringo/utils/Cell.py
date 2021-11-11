from utils import Token, Ring, Pawn, Board

class Cell:
    def __init__(self, index) -> None:
        self._is_occupied = False
        self._index = index
        self._ring = None
        self._pawn = None

    def get_ring(self) -> Ring:
        return self._ring

    def get_pawn(self) -> Pawn:
        return self._pawn

    def get_index(self) -> tuple:
        return self._index

    def get_token(self) -> Token:
        if self._pawn is not None:
            return self._pawn
        elif self._ring is not None:
            return self._ring
        else:
            return None

    def is_occupied(self) -> bool:
        return self._is_occupied

    def add_ring(self, ring: Ring) -> None:
        self._is_occupied = True
        self._ring = ring

    def add_pawn(self, pawn: Pawn) -> Ring:
        self._pawn = pawn
        ring = self._ring
        self._ring = None
        return ring

    def remove_pawn(self) -> Pawn:
        pawn = self._pawn
        self._pawn = None
        self._is_occupied = False
        return pawn

    def can_receive_pawn(self) -> bool:
        return (self._ring is not None)

    def can_receive_ring(self, board: Board) -> bool:
        return (not self._is_occupied and board.check_adjacents(self))

    def can_remove_pawn(self, board: Board, player_color: tuple) -> bool:
        pawn = self._pawn
        return (pawn is not None and pawn.get_color() == player_color and
                board.check_connected_components(self))

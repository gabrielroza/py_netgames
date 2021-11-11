from utils.Pawn import Pawn


class Player:
    def __init__(self, number, color):
        self._name = ""

        self._number = number

        self._color = color
        self._pawns = self._populate_pawns()
        self._ring = None

        self._is_my_turn = False
        self._pawn_placed = False
        self._pawn_removed = False

    def set_turn(self) -> None:
        self._is_my_turn = True

    def has_name(self) -> bool:
        return self.get_name() != ""

    def is_my_turn(self) -> bool:
        return self._is_my_turn

    def switch_turn(self) -> None:
        self._is_my_turn = not self._is_my_turn

    def is_pawn_placed(self) -> bool:
        return self._pawn_placed

    def is_pawn_removed(self) -> bool:
        return self._pawn_removed

    def reset_pawn_placed(self):
        self._pawn_placed = False

    def reset_pawn_removed(self):
        self._pawn_removed = False

    def get_ring(self):
        return self._ring

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = ''.join(name)

    def get_color(self):
        return self._color

    def get_number(self) -> int:
        return self._number

    def get_pawns(self):
        return self._pawns

    def _populate_pawns(self):
        pawns = []
        for i in range(10):
            pawns.append(Pawn(self._color, 12))

        return pawns

    def remove_pawn(self, selected_position) -> None:
        pawn = selected_position.remove_pawn()
        self._pawns.append(pawn)
        self._pawn_removed = True

    def put_pawn(self, selected_position) -> None:
        self._ring = selected_position.add_pawn(self._pawns.pop())
        self._pawn_placed = True

    def put_ring(self, selected_position) -> None:
        ring = self._ring
        self._ring = None
        selected_position.add_ring(ring)

    def end_turn(self) -> None:
        self._is_my_turn = False

    def reset(self):
        del self._pawns[:]
        self._pawns = self._populate_pawns()
        self._ring = None
        self._is_my_turn = False
        self._pawn_placed = False
        self._pawn_removed = False

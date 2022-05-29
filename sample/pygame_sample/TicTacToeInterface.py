from gameclient.pygameclient.PygameWebsocketProxy import PygameWebsocketProxy

from tictactoe.TicTacToeBoard import TicTacToeBoard


class TicTacToeInterface:
    _board: TicTacToeBoard
    _websocket: PygameWebsocketProxy
    _is_turn: bool

    def __init__(self, position: int) -> None:
        super().__init__()
        self._is_turn = position == 0
        if self._is_turn:
            self._board = TicTacToeBoard()

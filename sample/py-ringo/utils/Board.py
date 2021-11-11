from utils.Token import Token
from utils.Ring import Ring
from utils.Cell import Cell
from utils.utils import ORANGE, BLUE
from queue import Queue
from copy import deepcopy


class Board:
    def __init__(self) -> None:
        self._size = 15
        self._positions = self._init_board()
        self._populate_board()

    def get_positions(self) -> list:
        return self._positions

    def _init_board(self) -> list:
        positions = []
        for i in range(self._size):
            positions.append([])
            for j in range(self._size):
                pos = Cell((i, j))
                positions[i].append(pos)

        return positions

    def _populate_board(self) -> None:
        middle = int(self._size/2)
        for i in range(middle - 1, middle + 2):
            for j in range(middle - 1, middle + 2):
                if (i + j) % 2 == 0:
                    color = ORANGE
                else:
                    color = BLUE
                if not(i == j == middle):
                    ring = Ring(color, 18)
                    self._positions[i][j].add_ring(ring)

    # vai verificar se o jogador q fez a jogada atual ganhou
    # chama `check_column`, `check_line` e `check_diagonal`
    def check_winner(self, position: Cell) -> bool:
        return (self._check_column(position) or self._check_line(position) or self._check_diagonals(position))

    # verifica se existem 4 peças alinhadas na vertical
    # que possuam a mesma cor
    def _check_column(self, position: Cell) -> bool:
        aligned_tokens = 0
        token = position.get_token()
        (x, y) = position.get_index()
        for i in range(-3, 4):
            if 0 <= y + i < self._size and self.compare_tokens(token, self._positions[x][y + i].get_token()):
                aligned_tokens += 1
                if aligned_tokens == 4:
                    return True
            else:
                aligned_tokens = 0

        return False

    # verifica se existem 4 peças alinhadas na horizontal
    # que possuam a mesma cor
    def _check_line(self, position: Cell) -> bool:
        aligned_tokens = 0
        token = position.get_token()
        (x, y) = position.get_index()
        for i in range(-3, 4):
            if 0 <= x + i < self._size and self.compare_tokens(token, self._positions[x + i][y].get_token()):
                aligned_tokens += 1
                if aligned_tokens == 4:
                    return True
            else:
                aligned_tokens = 0

        return False

    # verifica se existem 4 peças alinhadas na diagonal
    # que possuam a mesma cor
    def _check_diagonals(self, position: Cell) -> bool:
        aligned_tokens = 0
        token = position.get_token()
        (x, y) = position.get_index()
        for i in range(-3, 4):
            if 0 <= x + i < self._size and 0 <= y + i < self._size and \
                    self.compare_tokens(token, self._positions[x + i][y + i].get_token()):
                aligned_tokens += 1
                if aligned_tokens == 4:
                    return True
            else:
                aligned_tokens = 0

        aligned_tokens = 0
        for i in range(-3, 4):
            if 0 <= x + i < self._size and 0 <= y - i < self._size and \
                    self.compare_tokens(token, self._positions[x + i][y - i].get_token()):
                aligned_tokens += 1
                if aligned_tokens == 4:
                    return True
            else:
                aligned_tokens = 0

        return False

    def compare_tokens(self, token1: Token, token2: Token) -> bool:
        if type(token1) == type(token2) and token1.get_color() == token2.get_color():
            return True
        else:
            return False

    # verifica se ao remover a peça da posição seleciona irá gerar
    # dois conjuntos no tabuleiro (problema de componentes conexas)
    def check_connected_components(self, selected_position: Cell) -> bool:
        (x, y) = selected_position.get_index()
        paths = Queue(28)                   # criação de uma pilha para controle de posições a serem visitadas
        board = deepcopy(self._positions)   # realiza uma cópia do tabuleiro atual
        board[x][y] = Cell((x, y))          # reseta a posição selecionada
        connected_components_count = 0
        R = [[0] * self._size for _ in range(self._size)]   # matriz de controle para posições já visitadas
        for row in range(0, self._size):
            for column in range(0, self._size):
                if board[row][column].is_occupied() and not R[row][column]:
                    connected_components_count += 1
                    if connected_components_count >= 2:
                        return False
                    R[row][column] = connected_components_count
                    paths.put((row, column))

                    while not paths.empty():
                        (x, y) = paths.get()
                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                if 0 <= x + i < self._size and 0 <= y + j < self._size \
                                        and not R[x + i][y + j] and board[x + i][y + j].is_occupied():
                                    R[x + i][y + j] = connected_components_count
                                    paths.put((x + i, y + j))

        return True

    def check_adjacents(self, selected_position: Cell) -> bool:
        (x, y) = selected_position.get_index()
        for i in range(-1, 2, 2):
            if (0 <= x + i < self._size and self._positions[x + i][y].is_occupied()) or \
                    (0 <= y + i < self._size and self._positions[x][y + i].is_occupied()):
                return True

        return False

    def reset(self) -> None:
        del self._positions[:]
        self._positions = self._init_board()
        self._populate_board()

from typing import Tuple, List

import pygame
from gameclient.pygameclient.PygameWebsocketProxy import PygameWebsocketProxy

from tictactoe.TicTacToeBoard import TicTacToeBoard
from tictactoe.TicTacToeMark import TicTacToeMark
from pygame_sample import WINDOW_WIDTH, WINDOW_HEIGHT


class TicTacToeInterface:
    _board: TicTacToeBoard
    _websocket: PygameWebsocketProxy
    _is_turn: bool
    _mark: TicTacToeMark
    _is_running: bool
    _surface: pygame.Surface

    def __init__(self, position: int, surface: pygame.Surface) -> None:
        super().__init__()
        self._is_turn = position == 0
        self._mark = TicTacToeMark.CROSS if self._is_turn else TicTacToeMark.CIRCLE
        self._surface = surface
        if self._is_turn:
            self._board = TicTacToeBoard()
        self._is_running = True
        self._setup()
        self._run()

    def _setup(self):
        self._surface.fill((255, 255, 255))
        line_thickness = 7
        line_coordinates: List[List[Tuple[float, float]]] = [
            [(WINDOW_WIDTH / 3, 0), (WINDOW_WIDTH / 3, WINDOW_HEIGHT)],
            [(WINDOW_WIDTH / 3 * 2, 0), (WINDOW_WIDTH / 3 * 2, WINDOW_HEIGHT)],
            [(0, WINDOW_HEIGHT / 3), (WINDOW_WIDTH, WINDOW_HEIGHT / 3)],
            [(0, WINDOW_HEIGHT / 3 * 2), (WINDOW_WIDTH, WINDOW_HEIGHT / 3 * 2)]
        ]
        for start_pos, end_pos in line_coordinates:
            pygame.draw.line(self._surface, (0, 0, 0), start_pos, end_pos, line_thickness)

        pygame.display.update()

    def _run(self):
        while self._is_running:
            events = pygame.event.get()
            for event in events:
                print(event)

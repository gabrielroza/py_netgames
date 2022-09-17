from pathlib import Path
from typing import Tuple, List, Literal, Optional

import pygame
from py_netgames_client.pygame_client.PyNetgamesServerProxy import PyNetgamesServerProxy, MOVE_RECEIVED, \
    CONNECTION_ERROR
from py_netgames_model.messaging.message import MatchStartedMessage, MoveMessage
from pygame import MOUSEBUTTONDOWN
from pygame.font import Font
from pygame.image import load
from pygame.transform import scale

from pygame_sample import WINDOW_WIDTH, WINDOW_HEIGHT
from tictactoe.TicTacToeBoard import TicTacToeBoard, TicTacToeCoordinate
from tictactoe.TicTacToeMark import TicTacToeMark


class TicTacToeInterface:
    _board: TicTacToeBoard
    _server_proxy: PyNetgamesServerProxy
    _is_running: bool
    _surface: pygame.Surface

    def __init__(self, message: MatchStartedMessage, surface: pygame.Surface, server_proxy: PyNetgamesServerProxy) -> None:
        super().__init__()
        self.match_id = message.match_id
        self._surface = surface
        self._server_proxy = server_proxy
        self._board = TicTacToeBoard(message.position)
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
        self._update_screen()
        pygame.display.update()

    def _run(self):
        while self._is_running:
            events = pygame.event.get()
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    self._handle_click(pygame.mouse.get_pos())
                elif event.type == MOVE_RECEIVED:
                    self._handle_move_received(event.message)
                elif event.type == CONNECTION_ERROR:
                    self._is_running = False

    def _handle_click(self, mouse_position: Tuple[int, int]):
        clicked_board_coordinate = self._get_board_coordinate_from_click(mouse_position)
        marked = self._board.mark(clicked_board_coordinate) if clicked_board_coordinate is not None else False

        if marked:
            self._server_proxy.send_move(self.match_id, self._board.to_dict())
            self._update_screen()

    def _get_board_coordinate_from_click(self, mouse_position: Tuple[int, int]) -> Optional[TicTacToeCoordinate]:
        x, y = mouse_position

        def get_position(absolute_size, position) -> Optional[Literal[0, 1, 2]]:
            first_third = absolute_size / 3
            middle = absolute_size / 3 * 2
            return 0 if position < first_third else 1 if position < middle else 2 if position < absolute_size else None

        board_coordinate = get_position(WINDOW_HEIGHT, y), get_position(WINDOW_WIDTH, x)
        return None if any(position is None for position in board_coordinate) else board_coordinate

    def _handle_move_received(self, message: MoveMessage):
        self._board = TicTacToeBoard.from_dict(message.payload).flip()
        self._update_screen()

    def _update_screen(self):
        state = self._board.get_state()
        text = Font(None, 50).render(state.description, True, (255, 255, 255))
        self._surface.fill((0, 0, 0), pygame.Rect(0, WINDOW_WIDTH, WINDOW_WIDTH, 100))
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.03))
        self._surface.blit(text, text_rect)

        def load_image(relative_path: str):
            return scale(load(str(Path(__file__).parent / relative_path)), (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4))

        image_by_mark = {
            TicTacToeMark.CROSS: load_image("../assets/X.png"),
            TicTacToeMark.CIRCLE: load_image("../assets/O.png"),
        }

        row_positions = {
            0: 30,
            1: WINDOW_WIDTH / 3 + 30,
            2: WINDOW_WIDTH / 3 * 2 + 30
        }

        column_positions = {
            0: 30,
            1: WINDOW_HEIGHT / 3 + 30,
            2: WINDOW_HEIGHT / 3 * 2 + 30
        }

        for (row_index, column_index), mark in self._board.get_filled_coordinates().items() if self._board else []:
            self._surface.blit(image_by_mark[mark], (column_positions[column_index], row_positions[row_index]))

        pygame.display.update()

        if state.game_over:
            pygame.time.wait(3000)
            self._server_proxy.send_disconnect()
            self._is_running = False

from typing import Tuple, List, Literal, Optional

import pygame
from gameclient.pygameclient.PygameWebsocketProxy import PygameWebsocketProxy, MOVE_RECEIVED, CONNECTION_ERROR
from model.messaging.message import MatchStartedMessage, MoveMessage
from pygame import MOUSEBUTTONDOWN
from pygame.font import Font

from pygame_sample import WINDOW_WIDTH, WINDOW_HEIGHT
from tictactoe.StalemateException import StalemateException
from tictactoe.TicTacToeBoard import TicTacToeBoard, TicTacToeCoordinate
from tictactoe.TicTacToeMark import TicTacToeMark


class TicTacToeInterface:
    _board: TicTacToeBoard
    _websocket: PygameWebsocketProxy
    _is_turn: bool
    _mark: TicTacToeMark
    _is_running: bool
    _surface: pygame.Surface

    def __init__(self, message: MatchStartedMessage, surface: pygame.Surface, websocket: PygameWebsocketProxy) -> None:
        super().__init__()
        self.match_id = message.match_id
        self._is_turn = message.position == 0
        self._mark = TicTacToeMark.CROSS if self._is_turn else TicTacToeMark.CIRCLE
        self._surface = surface
        self._websocket = websocket
        self._board = TicTacToeBoard() if self._is_turn else None
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
        if self._is_turn:
            board_coordinate = self._get_board_coordinate_from_click(mouse_position)
            marked = self._board.mark(self._mark, board_coordinate) if board_coordinate is not None else False

            if marked:
                self._update_screen()
                self._websocket.send_move(self.match_id, self._board.to_json())
                self._is_turn = False

    def _get_board_coordinate_from_click(self, mouse_position: Tuple[int, int]) -> Optional[TicTacToeCoordinate]:
        x, y = mouse_position

        def get_position(absolute_size, position) -> Optional[Literal[0, 1, 2]]:
            first_third = absolute_size / 3
            middle = absolute_size / 3 * 2
            return 0 if position < first_third else 1 if position < middle else 2 if position < absolute_size else None

        board_coordinate = get_position(WINDOW_HEIGHT, y), get_position(WINDOW_WIDTH, x)
        print(board_coordinate)
        return None if any(position is None for position in board_coordinate) else board_coordinate

    def _handle_move_received(self, message: MoveMessage):
        self._board = TicTacToeBoard.from_json(message.payload)
        self._is_turn = True
        self._update_screen()

    def _update_screen(self):

        def evaluate_message() -> str:
            if self._is_turn:
                return "Make your move"
            else:
                try:
                    if self._board and self._board.get_winner():
                        return self._board.get_winner().value + " won"
                    else:
                        return "Awaiting opponent's move"
                except StalemateException:
                    return "Draw"

        text = Font(None, 50).render(evaluate_message(), True, (255, 255, 255))
        self._surface.fill((0, 0, 0), pygame.Rect(0, WINDOW_WIDTH, WINDOW_WIDTH, 100))
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.03))
        self._surface.blit(text, text_rect)
        pygame.display.update()

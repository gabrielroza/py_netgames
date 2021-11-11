from pygame import draw, font, display, Surface, Rect
from utils.utils import LIGHTGREY


class View:
    def __init__(self) -> None:
        self._init_screen()

    def _init_screen(self) -> None:
        dimensions: tuple = (1280, 720)
        self._screen: Surface = display.set_mode(dimensions)
        self._background: Surface = self._screen.convert()
        self._font: font.Font = font.SysFont('arial', 20, False)
        self._antialias: bool = True

        display.set_caption("Py-Ringo")
        self._background.fill(LIGHTGREY)

    def draw_welcome_screen(self) -> None:
        self._draw_background()
        self._draw_text("Welcome to Py-Ringo!", (0.5, 0.4))
        self._draw_text("Press Enter to continue.", (0.5, 0.9))

        display.flip()

    def _draw_text(self, string: str, relative_position: tuple, color: tuple = (16, 137, 86)) -> None:
        text: Surface = self._font.render(string, self._antialias, color)
        position: Rect = text.get_rect(
            center=self._get_position(relative_position)
        )

        self._screen.blit(text, position)

    def _get_position(self, relative_position: tuple) -> tuple:
        (relative_x, relative_y) = relative_position
        x: float = self._screen.get_width()*relative_x
        y: float = self._screen.get_height()*relative_y

        return x, y

    def _draw_background(self) -> None:
        position: tuple = (0, 0)
        self._screen.blit(self._background, position)

    def draw_query_screen(self, player_num: int, text_input: str, feedback: str) -> None:
        self._draw_background()
        message = f"Player {player_num}, enter your name:"
        self._draw_text(message, (0.5, 0.05))
        self._draw_text(text_input, (0.5, 0.4))
        self._draw_text("Press Enter to confirm.", (0.5, 0.9))
        if feedback:
            self._draw_text(feedback, (0.5, 0.6), (211, 33, 45))

        display.flip()

    def draw_game(self, positions: list, p1, p2, message: str, round_counter: int, feedback: str) -> None:
        p1_name = p1.get_name()
        p2_name = p2.get_name()
        p1_pawns = p1.get_pawns()
        p2_pawns = p2.get_pawns()
        p1_ring = p1.get_ring()
        p2_ring = p2.get_ring()
        self._draw_background()
        self._draw_text(p1_name, (0.06, 0.05))
        self._draw_text(p2_name, (0.94, 0.05))
        self._draw_text(message, (0.5, 0.03))
        round_msg = "Round: " + str(round_counter)
        self._draw_text(round_msg, (0.3, 0.95))
        if feedback:
            self._draw_text(feedback, (0.6, 0.95), (211, 33, 45))
        self._draw_player_tokens(p1_pawns, 30, p1_ring)
        self._draw_player_tokens(p2_pawns, self._screen.get_width() - 70, p2_ring)
        self._draw_board(positions)

        display.flip()

    def _draw_player_tokens(self, pawns: list, x: int, ring) -> None:
        y = 50
        size_of_position = 40
        for pawn in pawns:
            self._draw_pawn(pawn, y, x, size_of_position)
            y += 30

        if ring:
            self._draw_ring(ring, y, x, size_of_position)

    def _draw_board(self, positions) -> None:
        size_of_position = 40
        numbers_of_positions = 15
        size = size_of_position * numbers_of_positions
        start = ((self._screen.get_width() - size) / 2, (self._screen.get_height() - size) / 2)
        for row in positions:
            for position in row:
                self._draw_cell(position, start, size_of_position)

    def _draw_cell(self, cell, start, size_of_position) -> None:
        (i, j) = cell.get_index()
        x = size_of_position*i+start[1]
        y = size_of_position*j+start[0]
        draw.rect(self._screen, (175, 175, 175), Rect(y, x, size_of_position, size_of_position), 2)
        if cell.is_occupied():
            ring = cell.get_ring()
            pawn = cell.get_pawn()
            if ring:
                self._draw_ring(ring, x, y, size_of_position)
            if pawn:
                self._draw_pawn(pawn, x, y, size_of_position)

    def _draw_ring(self, ring, x, y, size_of_position) -> None:
        color: tuple = ring.get_color()
        radius: float = ring.get_radius()

        draw.circle(self._screen, color, (y + size_of_position / 2, x + size_of_position / 2), radius, 3)

    def _draw_pawn(self, pawn, x, y, size_of_position) -> None:
        color = pawn.get_color()
        radius = pawn.get_radius()

        draw.circle(self._screen, color, (y + size_of_position / 2, x + size_of_position / 2), radius)

    def draw_winning_screen(self, winner) -> None:
        self._draw_background()
        self._draw_text(f"{winner} ganhou a partida", (0.5, 0.4))
        self._draw_text(f"Aperte Enter para jogar novamente", (0.5, 0.9))

        display.flip()

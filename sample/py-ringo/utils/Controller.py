import pygame
from utils.View import View
from utils.Player import Player
from utils.utils import ORANGE, BLUE
from utils.Board import Board

class Controller:
    def __init__(self) -> None:
        pygame.init()
        self._init_state_attributes()
        self._init_components()
        self._init_attributes()

    def _init_state_attributes(self) -> None:
        self._quit: bool = False
        self._winner: bool = False
        self._is_running: bool = True
        self._is_playing: bool = False
        self._is_on_welcome_screen: bool = False
        self._is_waiting_for_names: bool = False

    def _init_attributes(self) -> None:
        self._char_input: str = []
        self._game_state_msg: str = ""
        self._error_feedback: str = ""
        self._winner_name: str = ""
        self._round: int = 1

    def _init_components(self) -> None:
        self._clock: pygame.Clock = pygame.time.Clock()
        self._view: View = View()
        self._player_one: Player = Player(1, ORANGE)
        self._player_two: Player = Player(2, BLUE)
        self._board: Board = Board()

    def _tick_clock(self) -> None:
        self._clock.tick(60)

    def _turn_off(self) -> None:
        self._quit = True
        self._winner = False
        self._is_running = False
        self._is_playing = False
        self._is_on_welcome_screen = False
        self._is_waiting_for_names = False

    def __del__(self) -> None:
        pygame.quit()

    def _set_error_feedback(self, message: str) -> None:
        self._error_feedback = message

    def _clear_error_feedback(self) -> None:
        if self._error_feedback:
            self._error_feedback = ""

    def run(self) -> None:
        while self._is_running:
            self._display_welcome_screen()
            self._query_player_names()
            self._play_game()
            self._display_winner_screen()

    def _display_welcome_screen(self) -> None:
        self._is_on_welcome_screen = True

        while self._is_on_welcome_screen:
            self._tick_clock()
            self._handle_welcome_screen_events()
            self._update_welcome_screen()

    def _handle_welcome_screen_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._turn_off()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._end_welcome_screen_state()

    def _end_welcome_screen_state(self) -> None:
        self._is_on_welcome_screen = False
        self._is_waiting_for_names = True

    def _update_welcome_screen(self) -> None:
        self._view.draw_welcome_screen()

    def _query_player_names(self) -> None:
        while self._is_waiting_for_names:
            self._query_name(self._player_one)
            self._query_name(self._player_two)
            self._end_query_player_names_state()

    def _query_name(self, player: Player) -> None:
        while not player.has_name() and not self._quit:
            self._tick_clock()
            self._handle_query_name_events(player)
            self._update_query_name_screen(player.get_number())

    def _handle_query_name_events(self, player: Player) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._turn_off()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not self._char_input:
                        self._set_error_feedback("Empty name not valid!")
                    else:
                        self._clear_error_feedback()
                        self._set_player_name(player)
                else:
                    self._get_text_input(event)

    def _set_player_name(self, player: Player) -> None:
        text_input: str = "".join(self._char_input)
        self._char_input = []
        player.set_name(text_input)

    def _get_text_input(self, event: 'Event') -> None:
        if event.key != pygame.K_BACKSPACE:
            if 97 <= event.key <= 122:
                if len(self._char_input) < 10:
                    self._char_input.append(chr(event.key))
        else:
            if self._char_input:
                self._char_input.pop()

    def _update_query_name_screen(self, player_num: int):
        text_input = "".join(self._char_input)
        self._view.draw_query_screen(player_num, text_input, self._error_feedback)

    def _end_query_player_names_state(self) -> None:
        self._is_waiting_for_names = False
        if not self._quit:
            self._is_playing = True
            self._player_one.set_turn()

    def _play_game(self) -> None:
        while self._is_playing:
            self._play_turn(self._player_one)
            self._switch_turns(self._player_one, self._player_two)
            self._play_turn(self._player_two)
            self._switch_turns(self._player_two, self._player_one)
            self._round += 1

    def _switch_turns(self, end_player: Player, begin_player: Player) -> None:
        if not self._quit:
            end_player.reset_pawn_placed()
            begin_player.switch_turn()
            if self._round > 10:
                end_player.reset_pawn_removed()

    def _play_turn(self, player: Player) -> None:
        while player.is_my_turn() and not self._winner:
            if self._round <= 10:
                self._put_pawn_and_put_ring(player)
            else:
                if not player.is_pawn_removed():
                    self._handle_remove_pawn_events(player)
                    self._set_game_state_msg(f"{player.get_name()}, remove a pawn")
                else:
                    self._put_pawn_and_put_ring(player)

            self._tick_clock()
            self._update_game_screen()

    def _put_pawn_and_put_ring(self, player: Player) -> None:
        if not player.is_pawn_placed():
            self._handle_put_token_events(player)
            self._set_game_state_msg(f"{player.get_name()}, place the pawn in a ring")
        else:
            self._handle_put_token_events(player)
            self._set_game_state_msg(f"{player.get_name()}, place the ring")

    def _handle_put_token_events(self, player: Player) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.end_turn()
                self._turn_off()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = self._get_click_pos()
                for row in self._board.get_positions():
                    for position in row:
                        hitbox = self._get_position_hitbox(position)
                        if self._valid_click(click_pos, hitbox):
                            if not player.is_pawn_placed():
                                if position.can_receive_pawn():
                                    player.put_pawn(position)
                                    winner = self._board.check_winner(position)

                                    if winner:
                                        pawn = position.get_pawn()
                                        self._winner_name = self._get_name_of_winner(pawn.get_color())
                                        self._end_game_state()

                                    self._clear_error_feedback()
                                else:
                                    self._set_error_feedback("Invalid position. Please select a valid position")
                            else:
                                if position.can_receive_ring(self._board):
                                    player.put_ring(position)
                                    winner = self._board.check_winner(position)

                                    if winner:
                                        ring = position.get_ring()
                                        self._winner_name = self._get_name_of_winner(ring.get_color())
                                        self._end_game_state()

                                    player.switch_turn()
                                    self._clear_error_feedback()
                                else:
                                    self._set_error_feedback("Invalid position. Please select a valid position")

    def _get_click_pos(self):
        return pygame.mouse.get_pos()

    def _end_game_state(self) -> None:
        self._is_playing = False
        self._winner = True

    def _handle_remove_pawn_events(self, player: Player) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.end_turn()
                self._turn_off()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = self._get_click_pos()
                for row in self._board.get_positions():
                    for position in row:
                        hitbox = self._get_position_hitbox(position)
                        if self._valid_click(click_pos, hitbox):
                            if position.can_remove_pawn(self._board, player.get_color()):
                                player.remove_pawn(position)
                                self._clear_error_feedback()
                            else:
                                self._set_error_feedback("Cannot remove pawn from here!")

    def _valid_click(self, click_pos: tuple, hitbox: tuple) -> bool:
        (x0, y0, x1, y1) = hitbox
        return (x0 <= click_pos[1] <= x0 + x1) and (y0 <= click_pos[0] <= y0 + y1)

    def _update_game_screen(self) -> None:
        positions = self._board.get_positions()
        self._view.draw_game(self._board.get_positions(), self._player_one, self._player_two, self._game_state_msg, self._round, self._error_feedback)

    def _get_position_hitbox(self, position) -> tuple:
        size_of_position = 40
        numbers_of_positions = 15
        screen = (1280, 720)
        (i, j) = position.get_index()
        start = ((screen[0] - size_of_position * numbers_of_positions) / 2,
                 (screen[1] - size_of_position * numbers_of_positions) / 2)
        hitbox = (size_of_position * i + start[1], size_of_position * j + start[0], size_of_position, size_of_position)

        return hitbox

    def _set_game_state_msg(self, message: str) -> None:
        self._game_state_msg = message

    def _clear_game_state_msg(self) -> None:
        self._game_state_msg = ""

    def _get_name_of_winner(self, color_of_winner: tuple) -> str:
        if color_of_winner == self._player_one.get_color():
            return self._player_one.get_name()
        else:
            return self._player_two.get_name()

    def _display_winner_screen(self) -> None:
        while self._winner:
            self._tick_clock()
            self._handle_winning_screen_events()
            self._update_winning_screen()

    def _handle_winning_screen_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._turn_off()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._reset_game()

    def _reset_game(self) -> None:
        self._reset_components()
        self._reset_game_state_attributes()
        self._reset_attributes()
        self._player_one.set_turn()

    def _reset_components(self) -> None:
        self._player_one.reset()
        self._player_two.reset()
        self._board.reset()

    def _reset_game_state_attributes(self) -> None:
        self._is_waiting_for_names = False
        self._is_playing = True
        self._winner = False

    def _reset_attributes(self) -> None:
        self._char_input = []
        self._game_state_msg = ""
        self._error_feedback = ""
        self._winner_name = ""
        self._round = 1

    def _update_winning_screen(self) -> None:
        self._view.draw_winning_screen(self._winner_name)

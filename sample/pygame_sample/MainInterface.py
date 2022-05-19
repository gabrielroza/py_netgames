import pygame
import pygame_menu
from pygame_menu import Menu


class MainInterface:
    _is_running: bool
    _surface: pygame.Surface
    _main_menu: Menu

    def __init__(self) -> None:
        pygame.init()
        self._surface = pygame.display.set_mode([1024, 1080], pygame.RESIZABLE)
        self._main_menu = self._build_main_menu()
        self._is_running = True

    def run(self):
        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._is_running = False

            self._build_main_menu().mainloop(self._surface)

    def _build_main_menu(self):
        main_menu = pygame_menu.Menu('TicTacToe', 1024, 1080, theme=pygame_menu.themes.THEME_BLUE)
        main_menu.add.text_input('Server address: ', default='localhost:8765', textinput_id='address')
        main_menu.select_widget(main_menu.add.button('Connect', self._connect))
        main_menu.add.button('Quit', pygame_menu.events.EXIT)
        return main_menu

    def _connect(self):
        print(f"""Connecting to: {self._main_menu.get_widget("address").get_value()}""")
        pass

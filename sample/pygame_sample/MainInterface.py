import pygame
import pygame_menu
from pygame_menu import Menu

from pygame_sample.PygameWebsocketProxy import PygameWebsocketProxy, CONNECTED


class MainInterface:
    _is_running: bool
    _surface: pygame.Surface
    _main_menu: Menu
    _websocket: PygameWebsocketProxy

    def __init__(self) -> None:
        pygame.init()
        self._surface = pygame.display.set_mode([1024, 1080], pygame.RESIZABLE)
        self._main_menu = self._build_main_menu()
        self._is_running = True
        self._websocket = PygameWebsocketProxy()

    def run(self):
        while self._is_running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == CONNECTED:
                    print("CONNECTED!!!")

            if self._main_menu.is_enabled():
                self._main_menu.update(events)
                self._main_menu.draw(self._surface)

            pygame.display.update()

    def _build_main_menu(self):
        main_menu = pygame_menu.Menu('TicTacToe', 1024, 1080, theme=pygame_menu.themes.THEME_BLUE)
        main_menu.add.text_input('Server address: ', default='localhost:8765', textinput_id='address')
        main_menu.select_widget(main_menu.add.button('Connect', self._connect))
        main_menu.add.button('Quit', pygame_menu.events.EXIT)
        main_menu.enable()
        return main_menu

    def _connect(self):
        print(f"""Connecting to: {self._main_menu.get_widget("address").get_value()}""")
        self._websocket.connect(self._main_menu.get_widget("address").get_value())
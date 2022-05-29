import pygame
import pygame_menu
from gameclient.pygameclient.PygameWebsocketProxy import PygameWebsocketProxy, CONNECTED, CONNECTION_ERROR, DISCONNECTED
from pygame_menu import Menu
from pygame_menu.widgets import ToggleSwitch


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
                if event.type == CONNECTED:
                    self._main_menu.get_widget('connect').readonly = False
                    self._main_menu.get_widget('connect').set_value(2)
                elif event.type == DISCONNECTED:
                    self._main_menu.get_widget('connect').readonly = False
                    self._main_menu.get_widget('connect').set_value(0)
                elif event.type == CONNECTION_ERROR:
                    self._main_menu.get_widget('connect').readonly = False
                    self._main_menu.get_widget('connect').set_value(0)
                    print(event.message)

            if self._main_menu.is_enabled():
                self._main_menu.update(events)
                self._main_menu.draw(self._surface)

            pygame.display.update()

    def _build_main_menu(self):
        main_menu = pygame_menu.Menu('TicTacToe', 1024, 1080, theme=pygame_menu.themes.THEME_BLUE)
        main_menu.add.text_input('Server address: ', default='localhost:8765', textinput_id='address')
        main_menu.select_widget(main_menu.add.generic_widget(self._build_connect_switch(), configure_defaults=True))
        main_menu.add.button('Quit', pygame_menu.events.EXIT)
        main_menu.enable()
        return main_menu

    def _build_connect_switch(self) -> ToggleSwitch:
        return ToggleSwitch(title='Connection Status: ',
                            toggleswitch_id='connect',
                            single_click=True,
                            single_click_dir=False,
                            slider_thickness=0,
                            state_values=('Disconnected', 'Connecting', 'Connected', 'Disconnecting'),
                            state_color=((178, 178, 178), (206, 144, 0), (117, 185, 54), (206, 144, 0)),
                            state_text_font_color=((255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)),
                            state_width=(150, 150, 150),
                            state_text=('Disconnected', 'Connecting', 'Connected', 'Disconnecting'),
                            onchange=self._connect)

    def _connect(self, state: str):
        if state == 'Connecting':
            print(f"""Connecting to: {self._main_menu.get_widget("address").get_value()}""")
            self._websocket.connect(self._main_menu.get_widget("address").get_value())
            self._main_menu.get_widget('connect').readonly = True
        elif state == 'Disconnecting':
            self._websocket.disconnect()
            self._main_menu.get_widget('connect').set_value(3)
            self._main_menu.get_widget('connect').readonly = True

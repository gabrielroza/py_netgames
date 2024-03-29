import logging

import pygame
import pygame_menu
from py_netgames_client.pygame_client.PyNetgamesServerProxy import PyNetgamesServerProxy, CONNECTED, CONNECTION_ERROR, \
    DISCONNECTED, MATCH_REQUESTED, MATCH_STARTED
from pygame_menu import Menu
from pygame_menu.widgets import ToggleSwitch

from pygame_sample import WINDOW_WIDTH, WINDOW_HEIGHT
from pygame_sample.TicTacToeInterface import TicTacToeInterface


class MainInterface:
    _is_running: bool
    _surface: pygame.Surface
    _main_menu: Menu
    _server_proxy: PyNetgamesServerProxy
    _logger: logging.Logger

    def __init__(self) -> None:
        pygame.init()
        self._surface = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT], pygame.RESIZABLE)
        self._main_menu = self._build_main_menu()
        self._is_running = True
        self._server_proxy = PyNetgamesServerProxy()
        self._logger = logging.getLogger("pygame_sample.MainInterface")

    def run(self):
        while self._is_running:
            events = pygame.event.get()
            for event in events:
                if event.type == CONNECTED:
                    self._main_menu.get_widget('connect').readonly = False
                    self._main_menu.get_widget('connect').set_value(2)
                    self._main_menu.get_widget('request').readonly = False
                elif event.type == DISCONNECTED:
                    self._main_menu.get_widget('connect').readonly = False
                    self._main_menu.get_widget('connect').set_value(0)
                    self._main_menu.get_widget('request').readonly = True
                    self._main_menu.get_widget('request').set_value(0)
                elif event.type == CONNECTION_ERROR:
                    self._logger.error(event.message)
                    self._main_menu.get_widget('connect').readonly = False
                    self._main_menu.get_widget('connect').set_value(0)
                    self._main_menu.get_widget('request').readonly = True
                    self._main_menu.get_widget('request').set_value(0)
                elif event.type == MATCH_REQUESTED:
                    self._main_menu.get_widget('request').readonly = True
                    self._main_menu.get_widget('request').set_value(1)
                elif event.type == MATCH_STARTED:
                    TicTacToeInterface(event.message, self._surface, self._server_proxy)
                    self._main_menu.select_widget('connect')
                    self._main_menu.get_widget('connect').readonly = False
                    self._main_menu.get_widget('connect').set_value(0)
                    self._main_menu.get_widget('request').readonly = True
                    self._main_menu.get_widget('request').set_value(0)

            if self._main_menu.is_enabled():
                self._main_menu.update(events)
                self._main_menu.draw(self._surface)

            pygame.display.update()

    def _build_main_menu(self):
        main_menu = pygame_menu.Menu('TicTacToe', WINDOW_WIDTH, WINDOW_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
        main_menu.select_widget(main_menu.add.generic_widget(self._build_connect_switch(), configure_defaults=True))
        main_menu.add.generic_widget(self._build_match_request_switch(), configure_defaults=True)
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

    def _build_match_request_switch(self):
        switch = ToggleSwitch(title='Request Match: ',
                              toggleswitch_id='request',
                              single_click=True,
                              single_click_dir=False,
                              slider_thickness=0,
                              state_values=('Request', 'Awaiting players'),
                              state_color=((178, 178, 178), (206, 144, 0)),
                              state_text_font_color=((255, 255, 255), (255, 255, 255)),
                              state_width=270,
                              state_text=('Request', 'Awaiting players'),
                              onchange=self._request_match)
        switch.readonly = True
        return switch

    def _connect(self, state: str):
        if state == 'Connecting':
            self._server_proxy.send_connect(address="wss://py-netgames-server.fly.dev")
            self._main_menu.get_widget('connect').readonly = True
        elif state == 'Disconnecting':
            self._server_proxy.send_disconnect()
            self._main_menu.get_widget('connect').set_value(3)
            self._main_menu.get_widget('connect').readonly = True

    def _request_match(self, state: str):
        if state == 'Request':
            raise NotImplementedError()
        elif state == 'Awaiting players':
            self._server_proxy.send_match(
                amount_of_players=2
            )

import pygame


class ChallengeInterface:
    _is_running: bool
    _screen = pygame.display.set_mode([1024, 1080])

    def __init__(self) -> None:
        pygame.init()
        self._is_running = True

    def run(self):
        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._is_running = False
            self._screen.fill((0, 124, 124))
            pygame.draw.circle(self._screen, (0, 0, 255), (250, 250), 75)
            pygame.display.flip()


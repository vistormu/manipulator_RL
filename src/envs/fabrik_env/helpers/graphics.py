import pygame

from src.envs.fabrik_env.entities.chain import Chain
from src.envs.fabrik_env.entities.target import Target
from src.envs.core.coordinates import *

WHITE = (255, 255, 255)
BLACK = (47, 47, 47)
RED = (182, 69, 69)
GREEN = (69, 181, 69)

HEIGHT = 360
WIDTH = 360


class Graphics:

    def __init__(self) -> None:
        pass

    def init(self):
        pygame.init()
        pygame.display.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def render(self, chain: Chain, fingertip_target: Point, target: Target):
        # Background
        self.display.fill(WHITE)

        # Chain
        self._draw_chain(chain)

        # Fingertip target
        pygame.draw.circle(surface=self.display,
                           color=BLACK,
                           center=(fingertip_target.x*WIDTH,
                                   HEIGHT-fingertip_target.y*HEIGHT),
                           radius=5,
                           )

        # Target
        pygame.draw.circle(surface=self.display,
                           color=GREEN,
                           center=(target.position.x*WIDTH,
                                   HEIGHT-target.position.y*HEIGHT),
                           radius=10,
                           )

    def update(self, fps):
        pygame.event.pump()
        pygame.display.update()
        self.clock.tick(fps)

    def close(self):
        pygame.display.quit()
        pygame.quit()

    def _draw_chain(self, chain: Chain):
        for link in chain.links:
            pygame.draw.line(self.display,
                             RED,
                             (link.start.x*WIDTH, HEIGHT - link.start.y*HEIGHT),
                             (link.end.x*WIDTH, HEIGHT - link.end.y*HEIGHT),
                             width=4)
            # pygame.draw.circle(surface=self.display,
            #                    color=BLACK,
            #                    center=(link.end.x*WIDTH,
            #                            HEIGHT-link.end.y*HEIGHT),
            #                    radius=5,
            #                    )

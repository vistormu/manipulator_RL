import pygame

from src.env.core.coordinates import *
from src.env.entities.manipulator import Manipulator
from src.env.entities.target import Target

WHITE = (255, 255, 255)
BLACK = (47, 47, 47)
RED = (182, 69, 69)
GREEN = (69, 181, 69)

HEIGHT = 360
WIDTH = 360


class Graphics():

    def __init__(self) -> None:
        pass

    def init(self):
        pygame.init()
        pygame.display.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def render(self, robot: Manipulator, target: Target):
        self.display.fill(WHITE)

        self._draw_robot(robot)
        self._draw_target(target)

    def update(self, fps):
        pygame.event.pump()
        pygame.display.update()
        self.clock.tick(fps)

    def close(self):
        pygame.display.quit()
        pygame.quit()

    def _draw_robot(self, robot: Manipulator):
        link1_origin = Point(0, HEIGHT)
        link1_end = Point(int(robot.link1.x*WIDTH),
                          HEIGHT - int(robot.link1.y*WIDTH))
        link2_end = Point(int(robot.link2.x*WIDTH),
                          HEIGHT - int(robot.link2.y*WIDTH))

        pygame.draw.line(self.display, BLACK,
                         link1_origin, link1_end, 4)
        pygame.draw.line(self.display, RED, link1_end, link2_end, 4)

    def _draw_target(self, target: Target):
        pygame.draw.circle(
            surface=self.display,
            color=GREEN,
            center=(int(target.x*WIDTH), HEIGHT-int(target.y*WIDTH)),
            radius=int(target.size*WIDTH))

import pygame

from core.coordinates import *
from src.manipulator import *
from src.blob import *

WHITE = (255, 255, 255)
BLACK = (47, 47, 47)
RED = (182, 69, 69)
GREEN = (69, 181, 69)

HEIGHT = 360
WIDTH = 360


class Graphics():

    def __init__(self) -> None:
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))

    def render(self, robot: Manipulator, blob: Blob):

        self.display.fill(WHITE)

        self._draw_robot(robot)
        self._draw_blob(blob)

        pygame.display.flip()

    def _draw_robot(self, robot: Manipulator):
        link1_origin = Point(0, HEIGHT)
        link1_end = Point(int(robot.link1.x*WIDTH),
                          HEIGHT - int(robot.link1.y*WIDTH))
        link2_end = Point(int(robot.link2.x*WIDTH),
                          HEIGHT - int(robot.link2.y*WIDTH))

        pygame.draw.line(self.display, BLACK,
                         link1_origin, link1_end, 4)
        pygame.draw.line(self.display, RED, link1_end, link2_end, 4)

    def _draw_blob(self, blob: Blob):
        pygame.draw.circle(
            surface=self.display,
            color=GREEN,
            center=(int(blob.x*WIDTH), HEIGHT-int(blob.y*WIDTH)),
            radius=int(blob.size*WIDTH))

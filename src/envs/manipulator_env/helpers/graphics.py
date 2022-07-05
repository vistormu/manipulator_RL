import pygame
import numpy as np

from src.envs.core.coordinates import *
from src.envs.manipulator_env.entities.manipulator import Manipulator
from src.envs.manipulator_env.entities.target import Target

WHITE = (255, 255, 255)
BLACK = (47, 47, 47)
RED = (182, 69, 69)
GREEN = (69, 181, 69)

HEIGHT = 360
WIDTH = 360

background_img = pygame.image.load(
    'src/envs/manipulator_env/helpers/assets/background.png')
link1_img = pygame.image.load(
    'src/envs/manipulator_env/helpers/assets/link-1.png')
link2_img = pygame.image.load(
    'src/envs/manipulator_env/helpers/assets/link-2.png')
target_img = pygame.image.load(
    'src/envs/manipulator_env/helpers/assets/target.png')


class Graphics():

    def __init__(self) -> None:
        pass

    def init(self):
        pygame.init()
        pygame.display.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def render(self, robot: Manipulator, target: Target):
        # Background
        self.display.blit(background_img, (0, 0))

        # Manipulator
        self._draw_robot(robot)

        # Target
        self._draw_target(target)

    def update(self, fps):
        pygame.event.pump()
        pygame.display.update()
        self.clock.tick(fps)

    def close(self):
        pygame.display.quit()
        pygame.quit()

    def _draw_link(self, image, pos, originPos, angle):

        # offset from pivot to center
        image_rect = image.get_rect(
            topleft=(pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        # roatetd image center
        rotated_image_center = (
            pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(
            center=rotated_image_center)

        # rotate and blit the image
        self.display.blit(rotated_image, rotated_image_rect)

    def _draw_robot(self, robot: Manipulator):
        link1_origin = Point(0, HEIGHT)
        link1_end = Point(int(robot.link1.x*WIDTH),
                          HEIGHT - int(robot.link1.y*WIDTH))
        link2_end = Point(int(robot.link2.x*WIDTH),
                          HEIGHT - int(robot.link2.y*WIDTH))

        offset = Point(22, 22)

        self._draw_link(link1_img,
                        link1_origin,
                        offset,
                        robot.link1.q*180/np.pi)

        self._draw_link(link2_img,
                        link1_end,
                        offset,
                        robot.link1.q*180/np.pi+robot.link2.q*180/np.pi)

    def _draw_target(self, target: Target):

        target_img_scaled = pygame.transform.scale(target_img,
                                                   (int(WIDTH*target.size),
                                                    int(HEIGHT*target.size)))

        target_position = Point(int(target.x*WIDTH),
                                HEIGHT-int(target.y*HEIGHT))

        self.display.blit(target_img_scaled, target_position)

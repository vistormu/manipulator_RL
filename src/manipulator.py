import numpy as np

from core import logger
from core.coordinates import *


def _to_radians(angle: Angle) -> Angle:
    new_angle = np.multiply(angle, np.pi/180)

    return Angle(*new_angle)


class Manipulator():
    L1 = 0.5
    L2 = 0.5

    MAX_ANGLES = Angle(90, 180)

    def __init__(self) -> None:
        self.log = logger.Logger(f'{__class__.__name__}')
        self._init_pose()

    def __str__(self) -> str:
        return f'End efector at ({self.link2.x}, {self.link2.y})'

    def _init_pose(self) -> None:
        q1 = np.random.randint(0, self.MAX_ANGLES.q1)
        q2 = np.random.randint(0, self.MAX_ANGLES.q2)

        angle = Angle(q1, q2)

        self.set_to(angle, degrees=True)

    def set_to(self, angle: Angle, degrees=False) -> None:
        if degrees:
            angle = _to_radians(angle)

        clipped_angle = np.clip(angle, (0, 0), _to_radians(self.MAX_ANGLES))
        clipped_angle = Angle(*clipped_angle)

        x1, y1, x2, y2 = self._forward_kinematics(clipped_angle)

        self.link1 = Pose(x1, y1, clipped_angle.q1)
        self.link2 = Pose(x2, y2, clipped_angle.q2)

    def move_to(self, point: Point) -> None:
        if np.power(point.x, 2) + np.power(point.y, 2) > np.power(self.L1+self.L2, 2):
            self.log.error('cannot move to the requested position')
            return

        angle = self._inverse_kinematics(point)
        self.set_to(angle)

    def _forward_kinematics(self, angle: Angle):
        x1 = self.L1*np.cos(angle.q1)
        y1 = self.L1*np.sin(angle.q1)
        x2 = x1 + self.L2*np.cos(angle.q1+angle.q2)
        y2 = y1 + self.L2*np.sin(angle.q1+angle.q2)

        return x1, y1, x2, y2

    def _inverse_kinematics(self, point: Point) -> Angle:
        q2 = np.arccos((np.power(point.x, 2)+np.power(point.y, 2) -
                        np.power(self.L1, 2)-np.power(self.L2, 2))/(2*self.L1*self.L2))
        q1 = np.arctan2(point.y, point.x) - np.arctan2(self.L2 *
                                                       np.sin(q2), self.L1+self.L2*np.cos(q2))

        return Angle(q1, q2)

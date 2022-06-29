import numpy as np

from src.env.core.coordinates import *


class Manipulator():
    L1 = 0.5
    L2 = 0.5

    MAX_ANGLES = Angle(90, 180)

    def __init__(self) -> None:
        self._init_pose()

    def __repr__(self) -> str:
        return f'End efector at ({self.link2.x}, {self.link2.y})'

    def _init_pose(self) -> None:
        q1 = np.random.randint(0, self.MAX_ANGLES.q1)
        q2 = np.random.randint(0, self.MAX_ANGLES.q2)

        self.set_to(Angle(q1, q2).to_radians())

    def set_to(self, angle: Angle) -> None:

        clipped_angle = np.clip(angle, (0, 0), self.MAX_ANGLES.to_radians())
        clipped_angle = Angle(*clipped_angle)

        link1_pos, link2_pos = self._forward_kinematics(clipped_angle)

        self.link1 = Pose(*link1_pos, clipped_angle.q1)
        self.link2 = Pose(*link2_pos, clipped_angle.q2)
        self.fingertip_position = link2_pos

    def move_to(self, point: Point) -> None:
        if np.power(point.x, 2) + np.power(point.y, 2) > np.power(self.L1+self.L2, 2):
            print('cannot move to the requested position')
            return

        angle = self._inverse_kinematics(point)
        self.set_to(angle)

    def _forward_kinematics(self, angle: Angle):
        x1 = self.L1*np.cos(angle.q1)
        y1 = self.L1*np.sin(angle.q1)
        x2 = x1 + self.L2*np.cos(angle.q1+angle.q2)
        y2 = y1 + self.L2*np.sin(angle.q1+angle.q2)

        return Point(x1, y1), Point(x2, y2)

    def _inverse_kinematics(self, point: Point) -> Angle:
        q2 = np.arccos((np.power(point.x, 2)+np.power(point.y, 2) -
                        np.power(self.L1, 2)-np.power(self.L2, 2))/(2*self.L1*self.L2))
        q1 = np.arctan2(point.y, point.x) - np.arctan2(self.L2 *
                                                       np.sin(q2), self.L1+self.L2*np.cos(q2))

        return Angle(q1, q2)

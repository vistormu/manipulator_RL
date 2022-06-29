from typing import NamedTuple
import numpy as np


class Pose(NamedTuple):
    x: float
    y: float
    q: float


class Angle(NamedTuple):
    q1: float
    q2: float

    def __sub__(self, other):
        return Angle(self.q1 - other.q1, self.q2 - other.q2)

    def __add__(self, other):
        return Angle(self.q1 + other.q1, self.q2 + other.q2)

    def to_radians(self):
        return Angle(self.q1*np.pi/180, self.q2*np.pi/180)

    def to_degrees(self):
        return Angle(self.q1*180/np.pi, self.q2*180/np.pi)


class Point(NamedTuple):
    x: float
    y: float

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

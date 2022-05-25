import typing


class Pose(typing.NamedTuple):
    x: float
    y: float
    q: float


class Angle(typing.NamedTuple):
    q1: float
    q2: float


class Point(typing.NamedTuple):
    x: float
    y: float

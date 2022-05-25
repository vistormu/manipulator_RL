import enum

from core.coordinates import *


class Movement(enum.Enum):
    q1_cw = enum.auto()
    q1_ccw = enum.auto()
    q2_cw = enum.auto()
    q2_ccw = enum.auto()
    q1_q2_cw = enum.auto()
    q1_q2_ccw = enum.auto()
    q1_cw_q2_ccw = enum.auto()
    q1_ccw_q2_cw = enum.auto()


class Translator():
    def __init__(self) -> None:
        pass

    @ staticmethod
    def _get_movement(choice: int) -> Movement:

        assert 0 <= choice <= 7

        if choice == 0:
            movement = Movement.q1_cw
        elif choice == 1:
            movement = Movement.q1_ccw
        elif choice == 2:
            movement = Movement.q2_cw
        elif choice == 3:
            movement = Movement.q2_ccw
        elif choice == 4:
            movement = Movement.q1_q2_cw
        elif choice == 5:
            movement = Movement.q1_q2_ccw
        elif choice == 6:
            movement = Movement.q1_cw_q2_ccw
        elif choice == 7:
            movement = Movement.q1_ccw_q2_cw

        return movement

    def get_angle(self, choice: int) -> Angle:
        movement = self._get_movement(choice)

        next_q1 = 0
        next_q2 = 0

        q1_cw = (movement == Movement.q1_cw) or \
                (movement == Movement.q1_q2_cw) or \
                (movement == Movement.q1_cw_q2_ccw)

        q2_cw = (movement == Movement.q2_cw) or \
                (movement == Movement.q1_q2_cw) or \
                (movement == Movement.q1_ccw_q2_cw)

        q1_ccw = (movement == Movement.q1_ccw) or \
            (movement == Movement.q1_q2_ccw) or \
            (movement == Movement.q1_ccw_q2_cw)

        q2_ccw = (movement == Movement.q2_ccw) or \
            (movement == Movement.q1_q2_ccw) or \
            (movement == Movement.q1_cw_q2_ccw)

        if q1_cw:
            next_q1 -= 0.05  # TMP
        if q1_ccw:
            next_q1 += 0.05
        if q2_cw:
            next_q2 -= 0.05
        if q2_ccw:
            next_q2 += 0.05

        return Angle(next_q1, next_q2)

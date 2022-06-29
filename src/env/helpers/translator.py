import numpy as np

from src.env.core.coordinates import *


class Translator():
    def __init__(self) -> None:
        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([-1, 0]),
            2: np.array([0, 1]),
            3: np.array([0, -1]),
            4: np.array([1, 1]),
            5: np.array([-1, -1]),
            6: np.array([1, -1]),
            7: np.array([-1, 1]),
        }

        self._increment = 0.05

        self.output_size = len(self._action_to_direction)

    def get_angle(self, action: int) -> Angle:
        next_angles = self._action_to_direction[action] * self._increment

        return Angle(*next_angles)

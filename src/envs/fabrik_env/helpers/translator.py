import numpy as np

from src.envs.core.coordinates import *


class Translator:
    def __init__(self) -> None:
        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }

        self._increment = 0.05
        self.action_space_size = len(self._action_to_direction)

    def get_direction(self, action):
        next_direction = self._action_to_direction[action] * self._increment

        return Point(*next_direction)

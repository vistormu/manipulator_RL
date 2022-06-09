import numpy as np

from src.manipulator import Manipulator
from src.blob import Blob


class Controller():

    MOVE_PENALTY = 1
    FOOD_REWARD = 100
    WIGGLE_PENALTY = 10

    def __init__(self) -> None:
        self.previous_distance = 0

    def get_state(self, manipulator: Manipulator, blob: Blob):
        return self._get_distance_vector(manipulator, blob)

    def get_reward(self, manipulator: Manipulator, blob: Blob):
        reward = 0

        # Penalty for moving
        reward -= self.MOVE_PENALTY

        # Penalty for not reducing distance
        distance = self._get_distance_scalar(manipulator, blob)
        if distance > self.previous_distance:
            reward -= self.MOVE_PENALTY

        self.previous_distance = distance

        # # Penalty for not moving smoothly
        # if self.last_action != self.action:
        #     reward -= self.WIGGLE_PENALTY

        # Reward for reaching the objective
        if self._is_equal(manipulator, blob):
            reward += self.FOOD_REWARD

        return reward

    def is_done(self, manipulator: Manipulator, blob: Blob):
        return True if self._is_equal(manipulator, blob) else False

    @staticmethod
    def _get_distance_vector(manipulator: Manipulator, blob: Blob):
        distance = np.array((manipulator.link2.x - blob.x,
                             manipulator.link2.y - blob.y))

        return distance

    def _get_distance_scalar(self, manipulator: Manipulator, blob: Blob):
        distance = np.linalg.norm(self._get_distance_vector(manipulator, blob))

        return distance

    def _is_equal(self, manipulator: Manipulator, blob: Blob):
        return np.all(np.abs(self._get_distance_vector(manipulator, blob)) <= blob.size)

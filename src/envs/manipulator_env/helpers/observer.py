import numpy as np

from src.envs.manipulator_env.entities.manipulator import Manipulator
from src.envs.manipulator_env.entities.target import Target


class Observer():

    MOVE_PENALTY = 1
    FOOD_REWARD = 100

    def __init__(self) -> None:
        self.previous_distance = 0

    def get_obs(self, manipulator: Manipulator, target: Target):

        obs = np.array([
            np.cos(manipulator.link1.q),
            np.cos(manipulator.link2.q),
            np.sin(manipulator.link1.q),
            np.sin(manipulator.link2.q),
            target.position.x,
            target.position.y,
            (manipulator.fingertip_position - target.position).x,
            (manipulator.fingertip_position - target.position).y,
        ])

        return obs

    def get_reward(self, manipulator: Manipulator, target: Target):
        reward = 0

        # Penalty for moving
        reward -= self.MOVE_PENALTY

        # Penalty for not reducing distance
        distance = np.linalg.norm(
            np.array(manipulator.fingertip_position - target.position))
        if distance > self.previous_distance:
            reward -= self.MOVE_PENALTY

        self.previous_distance = distance

        # Reward for reaching the objective
        if self._is_equal(manipulator, target):
            reward += self.FOOD_REWARD

        return reward

    def is_done(self, manipulator: Manipulator, target: Target):
        return self._is_equal(manipulator, target)

    def get_info(self):
        return dict()

    def _is_equal(self, manipulator: Manipulator, target: Target):
        return np.all(np.abs(np.array(manipulator.fingertip_position - target.position)) <= target.size)

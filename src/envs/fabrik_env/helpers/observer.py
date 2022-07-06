import numpy as np

from src.envs.fabrik_env.entities.chain import Chain
from src.envs.fabrik_env.entities.target import Target


class Observer:

    MOVE_PENALTY = 1
    TARGET_REACHED_REWARD = 100

    def __init__(self) -> None:
        self.previous_distance = 0.0

    def get_obs(self, chain: Chain, target: Target):
        obs = np.array([
            chain.fingertip_position.x,
            chain.fingertip_position.y,
            target.position.x,
            target.position.y,
            chain.fingertip_position.x - target.position.x,
            chain.fingertip_position.y - target.position.y,
        ])

        return obs

    def get_reward(self, chain: Chain, target: Target):
        reward = 0

        # Penalty for moving
        reward -= self.MOVE_PENALTY

        # Penalty for not reducing distance
        distance = np.linalg.norm(
            np.array(chain.fingertip_position - target.position))
        if distance > self.previous_distance:
            reward -= self.MOVE_PENALTY

        self.previous_distance = distance

        # Reward for reaching the objective
        if self._is_equal(chain, target):
            reward += self.TARGET_REACHED_REWARD

        return reward

    def is_done(self, chain: Chain, target: Target):
        return self._is_equal(chain, target)

    def get_info(self):
        return dict()

    def _is_equal(self, chain: Chain, target: Target):
        return np.all(np.abs(np.array(chain.fingertip_position - target.position)) <= target.size)

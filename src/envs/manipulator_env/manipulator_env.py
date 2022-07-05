import gym
from gym import spaces

from src.envs.core.coordinates import *
from src.envs.manipulator_env.entities.manipulator import Manipulator
from src.envs.manipulator_env.helpers.graphics import Graphics
from src.envs.manipulator_env.entities.target import Target
from src.envs.manipulator_env.helpers.observer import Observer
from src.envs.manipulator_env.helpers.translator import Translator


class ManipulatorEnv(gym.Env):
    metadata = {"render_modes": ["human", ], "render_fps": 30}

    def __init__(self) -> None:
        self.manipulator = Manipulator()
        self.target = Target(size=0.05)
        self._observer = Observer()
        self._translator = Translator()
        self._graphics = Graphics()

        low = np.array([
            -1.0,  # cos(q1)
            -1.0,  # cos(q2)
            -1.0,  # sin(q1)
            -1.0,  # sin(q2)
            0.0,  # target.x
            0.0,  # target.y
            -1.0,  # fingertip.x - target.x
            -1.0,  # fingertip.y - target.y
        ]).astype(np.float32)

        high = np.array([
            1.0,  # cos(q1)
            1.0,  # cos(q2)
            1.0,  # sin(q1)
            1.0,  # sin(q2)
            1.0,  # target.x
            1.0,  # target.y
            1.0,  # fingertip.x - target.x
            1.0,  # fingertip.y - target.y
        ]).astype(np.float32)

        self.observation_space = spaces.Box(low, high)

        self.action_space = spaces.Discrete(
            self._translator.output_size)

    def reset(self, seed=None, return_info=False, options=None):
        super().reset(seed=seed)

        blob_x = self.np_random.uniform(low=0.0, high=0.5)
        blob_y = self.np_random.uniform(low=0.5, high=1.0)

        self.target.reset(blob_x, blob_y)
        # self.target.decay_size()

        observation = self._observer.get_obs(self.manipulator, self.target)
        info = self._observer.get_info()

        return (observation, info) if return_info else observation

    def step(self, action):
        # Translate from action to angle
        angle = Angle(self.manipulator.link1.q, self.manipulator.link2.q) + \
            self._translator.get_angle(action)

        # Move manipulator
        self.manipulator.set_to(angle)

        # Get new state, reward and done
        observation = self._observer.get_obs(self.manipulator, self.target)
        reward = self._observer.get_reward(self.manipulator, self.target)
        done = self._observer.is_done(self.manipulator, self.target)

        info = self._observer.get_info()

        return observation, reward, done, info

    def render(self, mode="human"):
        if mode == "human":
            self._graphics.init()
            self._graphics.render(self.manipulator, self.target)
            self._graphics.update(self.metadata["render_fps"])

    def close(self):
        self._graphics.close()

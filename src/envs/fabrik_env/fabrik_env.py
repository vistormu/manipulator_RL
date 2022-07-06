import gym
from gym import spaces

from src.envs.core.coordinates import *
from src.envs.fabrik_env.entities.chain import Chain
from src.envs.fabrik_env.entities.target import Target
from src.envs.fabrik_env.helpers.fabrik import Fabrik
from src.envs.fabrik_env.helpers.graphics import Graphics
from src.envs.fabrik_env.helpers.translator import Translator
from src.envs.fabrik_env.helpers.observer import Observer


class FabrikEnv(gym.Env):
    metadata = {"render modes": ["human"], "render_fps": 30}

    def __init__(self) -> None:
        links_number = 3
        points = []
        for i in range(links_number+1):
            point = Point(i/links_number, 0.0)
            points.append(point)

        self._chain = Chain(points)
        self._target = Target(size=0.05)
        self._fabrik = Fabrik()
        self._graphics = Graphics()
        self._translator = Translator()
        self._observer = Observer()
        self._fingertip_target = self._chain.fingertip_position

        low = np.array([
            -1.0,
            -1.0,
            -1.0,
            -1.0,
            -1.0,
            -1.0,
        ]).astype(np.float32)

        high = np.array([
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
        ]).astype(np.float32)

        self.observation_space = spaces.Box(low, high)
        self.action_space = spaces.Discrete(self._translator.action_space_size)
        self.observation_space_size = len(low)
        self.action_space_size = self._translator.action_space_size

        self.window = None

    def reset(self, seed=None, return_info=False, options=None):
        super().reset(seed=seed)

        target_x = self.np_random.uniform(low=0.0, high=0.5)
        target_y = self.np_random.uniform(low=0.5, high=1.0)
        self._target.reset(Point(target_x, target_y))

        observation = self._observer.get_obs(self._chain, self._target)
        info = self._observer.get_info()

        return (observation, info) if return_info else observation

    def step(self, action):
        self._fingertip_target += self._translator.get_direction(action)
        self._fingertip_target = Point(np.clip(self._fingertip_target.x, 0.0, 1.0),
                                       np.clip(self._fingertip_target.y, 0.0, 1.0))

        fabrik_done = False
        while not fabrik_done:
            new_chain, fabrik_done = self._fabrik.iterate(self._chain,
                                                          self._fingertip_target)

            if new_chain is None:
                break

            self._chain = new_chain

        observation = self._observer.get_obs(self._chain, self._target)
        reward = self._observer.get_reward(self._chain, self._target)
        done = self._observer.is_done(self._chain, self._target)
        info = self._observer.get_info()

        return observation, reward, done, info

    def render(self, mode="human"):
        if self.window is None and mode == "human":
            self._graphics.init()
            self.window = self._graphics.display

        if mode == "human":
            self._graphics.render(self._chain,
                                  self._fingertip_target,
                                  self._target)
            self._graphics.update(self.metadata["render_fps"])

    def close(self):
        self._graphics.close()

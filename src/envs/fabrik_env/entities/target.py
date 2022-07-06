import numpy as np

from src.envs.core.coordinates import *


class Target:

    def __init__(self, *, size) -> None:
        self.size: float = size

    def reset(self, position: Point):
        self.position = position

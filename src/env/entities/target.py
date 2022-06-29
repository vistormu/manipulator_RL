import numpy as np

from src.env.core.coordinates import *


class Target:
    DECAY_VALUE = 0.9999
    MIN_SIZE = 0.01

    def __init__(self, *, size) -> None:
        self.size: float = size

    def __repr__(self) -> str:
        return f'{__class__.__name__}({self.x}, {self.y})'

    def reset(self, x, y):
        self.x = x  # TMP
        self.y = y
        self.position = Point(x, y)

    def decay_size(self) -> None:
        self.size *= self.DECAY_VALUE
        self.size = np.clip(self.size, self.MIN_SIZE, 1)

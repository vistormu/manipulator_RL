import numpy as np


class Blob:
    DECAY_VALUE = 0.9999
    MIN_SIZE = 0.01

    def __init__(self, *, size) -> None:
        self.size: float = size
        self.reset()

    def __str__(self) -> str:
        return f'{__class__.__name__}({self.x}, {self.y})'

    def reset(self):
        self.x: float = np.random.rand()
        self.y: float = np.random.rand()
        self.x: float = np.clip(self.x, 0, 0.5)
        self.y: float = np.clip(self.y, 0.5, 1)

    def decay_size(self) -> None:
        self.size *= self.DECAY_VALUE
        self.size = np.clip(self.size, self.MIN_SIZE, 1)

import numpy as np


class Blob:

    def __init__(self, *, size) -> None:
        self.size: float = size

        self.x: float = np.random.rand()
        self.y: float = np.random.rand()
        self.x: float = np.clip(self.x, 0, 0.5)
        self.y: float = np.clip(self.y, 0.5, 1)

    def __str__(self) -> str:
        return f'{__class__.__name__}({self.x}, {self.y})'

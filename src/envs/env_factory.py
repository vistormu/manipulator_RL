from .fabrik_env.fabrik_env import FabrikEnv
from .manipulator_env.manipulator_env import ManipulatorEnv


def make(id: str):
    if id == "Fabrik-v0":
        return FabrikEnv()
    elif id == "Manipulator-v0":
        return ManipulatorEnv()

    raise Exception('Invalid agent type')

import numpy as np

from . import IAgent


class QAgent(IAgent):

    DISCOUNT = 0.95
    LEARNING_RATE = 0.1

    EPSILON_DECAY = 0.99975
    MIN_EPSILON = 0.001

    DISCRETE_OS_SIZE = [20, 20]

    def __init__(self, action_space_size) -> None:
        self.action_space_size = action_space_size
        self.q_table = np.random.uniform(low=-2,
                                         high=0,
                                         size=self.DISCRETE_OS_SIZE + [self.action_space_size])
        self.epsilon = 1

    def _get_discrete_state(self, state: np.ndarray) -> np.ndarray:
        discrete_state = (state * np.array(self.DISCRETE_OS_SIZE) / 2)

        return tuple(discrete_state.astype(int))

    def get_best_action(self, state: np.ndarray) -> int:

        discrete_state = self._get_discrete_state(state)

        if np.random.random() > self.epsilon:
            action = np.argmax(self.q_table[discrete_state])
        else:
            action = np.random.randint(0, self.action_space_size)

        return action

    def train(self, state, new_state, action, reward, done) -> None:
        discrete_state = self._get_discrete_state(state)
        new_discrete_state = self._get_discrete_state(new_state)

        if not done:
            max_future_q = np.max(self.q_table[new_discrete_state])
            current_q = self.q_table[discrete_state + (action,)]
            new_q = (1 - self.LEARNING_RATE) * current_q + \
                self.LEARNING_RATE * (reward + self.DISCOUNT * max_future_q)

            self.q_table[discrete_state + (action,)] = new_q
        else:
            self.q_table[discrete_state + (action,)] = 0

    def decay(self) -> None:
        if self.epsilon > self.MIN_EPSILON:
            self.epsilon *= self.EPSILON_DECAY
            self.epsilon = max(self.MIN_EPSILON, self.epsilon)

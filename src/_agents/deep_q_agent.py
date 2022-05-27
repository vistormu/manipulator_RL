import collections
import numpy as np
from keras import models, layers, optimizers

from . import IAgent

# DISCOUNT = 0.99
# REPLAY_MEMORY_SIZE = 50_000  # How many last steps to keep for model training
# MIN_REPLAY_MEMORY_SIZE = 1_000  # Minimum number of steps in a memory to start training
# MINIBATCH_SIZE = 64  # How many steps (samples) to use for training
# UPDATE_TARGET_EVERY = 5  # Terminal states (end of episodes)
# MODEL_NAME = '2x256'
# MIN_REWARD = -200  # For model save
# MEMORY_FRACTION = 0.20


class DeepQAgent(IAgent):

    REPLAY_MEMORY_SIZE = 50_000
    MIN_REPLAY_MEMORY_SIZE = 1000
    MINIBATCH_SIZE = 64

    EPSILON_DECAY = 0.99975
    MIN_EPSILON = 0.001

    def __init__(self, size) -> None:
        self.input_size, self.hidden_size, self.output_size = size

        self.model = self._create_model()

        self.target_model = self._create_model()
        self.target_model.set_weights(self.model.get_weights())

        self.replay_memory = collections.deque(maxlen=self.REPLAY_MEMORY_SIZE)

        self.target_update_counter = 0

        self.epsilon = 1

    def get_best_action(self, state):

        if np.random.random() > self.epsilon:
            action = self.model.predict(state)
            # self.model.predict(np.array(state).reshape(-1, *state.shape)/255)[0]
            pass
        else:
            action = np.random.randint(0, self.output_size)

        return action

    def update(self, state, new_state, action, reward, done):

        transition = [state, new_state, action, reward, done]

        # Update replay memory
        self.replay_memory.append(transition)

        # Start training only if certain number of samples is already saved
        if len(self.replay_memory) < self.MIN_REPLAY_MEMORY_SIZE:
            return

        minibatch = np.random.sample(self.replay_memory, self.MINIBATCH_SIZE)

        current_states = minibatch[0, :]
        current_qs = self.model.predict(current_states)
        new_current_states = minibatch[1, :]
        future_qs = self.model.predict(new_current_states)

        # WIP

    def decay(self) -> None:
        if self.epsilon > self.MIN_EPSILON:
            self.epsilon *= self.EPSILON_DECAY
            self.epsilon = max(self.MIN_EPSILON, self.epsilon)

    def _create_model(self):
        model = models.Sequential()

        # Input layer
        model.add(layers.Dense(self.input_size))
        model.add(layers.Activation('relu'))

        # Hidden layer
        model.add(layers.Dense(self.hidden_size))
        model.add(layers.Activation('relu'))

        # Output layer
        model.add(layers.Dense(self.output_size))
        model.add(layers.Activation('linear'))

        model.compile(loss='mse', optimizer=optimizers.adam_v2.Adam())

        return model

import collections
import random
import numpy as np
from keras import models, layers

from . import IAgent

from core import logger


class DeepQAgent(IAgent):

    REPLAY_MEMORY_SIZE = 50_000
    MIN_REPLAY_MEMORY_SIZE = 1000
    MINIBATCH_SIZE = 64

    UPDATE_TARGET_EVERY = 5

    EPSILON_DECAY = 0.99975
    MIN_EPSILON = 0.001

    DISCOUNT = 0.99

    def __init__(self, size) -> None:
        self.log = logger.Logger(__class__.__name__)

        self.input_size, self.hidden_size, self.output_size = size

        self.model = self._create_model()

        self.target_model = self._create_model()
        self.target_model.set_weights(self.model.get_weights())

        self.replay_memory = collections.deque(maxlen=self.REPLAY_MEMORY_SIZE)

        self.target_update_counter = 0

        self.epsilon = 1

    def get_best_action(self, state):

        if np.random.random() > self.epsilon:
            action = np.argmax(self.model.predict(
                state.reshape(-1, *state.shape))[0])
        else:
            action = np.random.randint(0, self.output_size)

        return action

    def update(self, state, new_state, action, reward, done):

        # Update replay memory
        transition = (state, new_state, action, reward, done)
        self.replay_memory.append(transition)

        # Start training only if certain number of samples is already saved
        if len(self.replay_memory) < self.MIN_REPLAY_MEMORY_SIZE:
            return

        minibatch = random.sample(self.replay_memory, self.MINIBATCH_SIZE)

        states, new_states, actions, rewards, dones = zip(*minibatch)
        current_qs = self.model.predict(np.array(states))
        future_qs = self.model.predict(np.array(new_states))

        X = []
        y = []

        for index, (state, new_state, action, reward, done) in enumerate(minibatch):

            if not done:
                max_future_q = np.max(future_qs[index])
                new_q = reward + self.DISCOUNT * max_future_q
            else:
                new_q = reward

            # Update Q value for given state
            current_q = current_qs[index]
            current_q[action] = new_q

            # And append to our training data
            X.append(state)
            y.append(current_q)

        # Fit on all samples as one batch
        self.model.fit(np.array(X),
                       np.array(y),
                       batch_size=self.MINIBATCH_SIZE,
                       verbose=0,
                       shuffle=False)

        # Update target network counter every episode
        if done:
            self.target_update_counter += 1

        # If counter reaches set value, update target network with weights of main network
        if self.target_update_counter > self.UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

    def decay(self) -> None:
        if self.epsilon > self.MIN_EPSILON:
            self.epsilon *= self.EPSILON_DECAY
            self.epsilon = max(self.MIN_EPSILON, self.epsilon)

    def _create_model(self):
        model = models.Sequential()

        # Input layer and first hidden layer
        model.add(layers.Dense(self.hidden_size,
                               input_dim=self.input_size,
                               activation='relu'))

        # Hidden layer
        model.add(layers.Dense(self.hidden_size,
                               activation='relu'))

        # Output layer
        model.add(layers.Dense(self.output_size,
                               activation='sigmoid'))

        # Compiler
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

        return model

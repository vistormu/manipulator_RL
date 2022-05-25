import time
import tqdm

from core import logger
from core.coordinates import *

from src.manipulator import Manipulator
from src.graphics import Graphics
from src.blob import Blob
from src.controller import Controller
from src.agent import Agent
from src.translator import Translator, Movement


def main():

    # Logger
    log = logger.Logger('main')
    log.init()

    # Constants
    EPISODES = 20_000
    SHOW_EVERY = 10_000
    MAX_EPISODES = 500

    # Entities
    manipulator = Manipulator()
    blob = Blob(size=0.1)
    controller = Controller()
    agent = Agent(action_space_size=len(Movement))
    translator = Translator()

    # Variables
    times_completed = 0

    # Graphics
    graphics = Graphics()

    for episode in tqdm.tqdm(range(1, EPISODES + 1), ascii=True, unit='episodes'):

        # Reset variables
        done = False
        episode_step = 0
        episode_reward = 0
        blob = Blob(size=0.1)

        # Get initial state
        state = controller.get_state(manipulator, blob)

        while not done:

            # Check max episodes and increase step
            if episode_step == MAX_EPISODES:
                break

            # Get best action
            action = agent.get_best_action(state)

            # Translate from action to angle
            angle_increment = translator.get_angle(action)
            angle = Angle(manipulator.link1.q + angle_increment.q1,
                          manipulator.link2.q + angle_increment.q2)

            # Move manipulator
            manipulator.set_to(angle)

            # Get new state, reward and done
            new_state = controller.get_state(manipulator, blob)
            reward = controller.get_reward(manipulator, blob)
            done = controller.is_done(manipulator, blob)

            # Update agent
            agent.update(state=state,
                         new_state=new_state,
                         action=action,
                         reward=reward,
                         done=done)

            # Update variables
            state = new_state
            episode_step += 1
            episode_reward += reward

            # Render
            if not episode % SHOW_EVERY:
                log.debug(f'{state=}, {episode_reward=}', flush=True)
                graphics.render(manipulator, blob)
                time.sleep(0.2)

        # Increase times completed counter if done
        if done:
            times_completed += 1

        # Decay epsilon
        agent.decay()

    log.info(f'{times_completed=}')


if __name__ == '__main__':
    main()

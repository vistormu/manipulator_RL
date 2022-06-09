import time
import tqdm

from core import logger
from core.coordinates import *

from src.manipulator import Manipulator
from src.graphics import Graphics
from src.blob import Blob
from src.controller import Controller
from src import agents
from src.translator import Translator


def main():

    # Logger
    log = logger.Logger('main')
    log.init()

    # Constants
    EPISODES = 20_000
    SHOW_EVERY = 100
    MAX_EPISODES = 500

    # Entities
    manipulator = Manipulator()
    blob = Blob(size=0.1)
    controller = Controller()
    translator = Translator()
    # agent = agents.get_agent(agent_type='q_agent',
    #                          action_space_size=translator.output_size)
    agent = agents.get_agent(agent_type='deep_q_agent',
                             size=(2, 24, translator.output_size))
    graphics = Graphics()

    # Variables
    times_completed = 0

    for episode in tqdm.tqdm(range(1, EPISODES + 1), ascii=True, unit='episodes'):
        # for episode in range(1, EPISODES+1):

        # Reset variables
        done = False
        episode_step = 0
        episode_reward = 0
        blob.reset()

        # Get initial state
        state = controller.get_state(manipulator, blob)

        while not done:

            # Check max episodes and increase step
            if episode_step >= MAX_EPISODES:
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

            # debug
            if episode > 1000:
                graphics.render(manipulator, blob)
                time.sleep(0.01)
            else:
                agent.train(state=state,
                            new_state=new_state,
                            action=action,
                            reward=reward,
                            done=done)

            # Train agent
            # agent.train(state=state,
            #             new_state=new_state,
            #             action=action,
            #             reward=reward,
            #             done=done)

            # Update variables
            state = new_state
            episode_step += 1
            episode_reward += reward

            # Render
            # if not episode % SHOW_EVERY:
            #     graphics.render(manipulator, blob)
            #     time.sleep(0.01)

        # Increase times completed counter if done
        if done:
            times_completed += 1

        # Decay epsilon
        agent.decay()
        blob.decay_size()

    log.info(f'{times_completed=}')


if __name__ == '__main__':
    main()

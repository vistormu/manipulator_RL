import tqdm

from core import logger
from src import agents
from src import envs
from src.save_info import Save


def main():

    # Logger
    log = logger.Logger('main')

    # Constants
    EPISODES = 1000
    SHOW_AFTER = 950
    MAX_EPISODES = 200

    # Entities
    env = envs.make('Fabrik-v0')
    agent = agents.get_agent(agent_type='deep_q_agent',
                             size=(env.observation_space_size, 64, env.action_space_size))  # TMP

    # save = Save(filename='results/results.csv',
    #             fieldnames=['episode', 'steps', 'rewards', 'done'])  # TMP

    # Variables
    times_completed = 0

    for episode in tqdm.tqdm(range(1, EPISODES + 1), unit='episodes'):
        # for episode in range(1, EPISODES+1):

        # Reset variables
        done = False
        episode_step = 0
        episode_reward = 0
        observation = env.reset()

        while not done:

            # Check max episodes and increase step
            if episode_step >= MAX_EPISODES:
                break

            # Get best action
            action = agent.get_best_action(observation)

            # log.debug(f'{action}', flush=True)

            new_observation, reward, done, _ = env.step(action)

            # Render or train
            if episode > SHOW_AFTER:
                env.render()
            else:
                agent.train(state=observation,
                            new_state=new_observation,
                            action=action,
                            reward=reward,
                            done=done)

            # Update variables
            observation = new_observation
            episode_step += 1
            episode_reward += reward

        # Increase times completed counter if done
        if done:
            times_completed += 1

        # Decay epsilon
        agent.decay()

        # Log info
        row = {
            'episode': episode,
            'steps': episode_step,
            'rewards': episode_reward,
            'done': 1 if done else 0,
        }

        # save.row(row)

    log.info(f'{times_completed=}')

    env.close()


if __name__ == '__main__':
    main()

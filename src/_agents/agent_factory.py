from . import QAgent, DeepQAgent


def get_agent(agent_type: str, *args, **kwargs):

    if agent_type == 'q_agent':
        return QAgent(*args, **kwargs)

    if agent_type == 'deep_q_agent':
        return DeepQAgent(*args, **kwargs)

    raise Exception('Invalid agent type')

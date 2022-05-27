import enum

from . import QAgent, DeepQAgent


class Agents(enum.Enum):
    q_agent = enum.auto()
    deep_q_agent = enum.auto()


class AgentFactory:

    @staticmethod
    def get_agent(agent_type: Agents, *args, **kwargs):

        if agent_type is Agents.q_agent:
            return QAgent(*args, **kwargs)

        if agent_type is Agents.deep_q_agent:
            return DeepQAgent(*args, **kwargs)

        raise Exception('Invalid agent type')

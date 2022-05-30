import abc


class IAgent(abc.ABC):

    @abc.abstractmethod
    def get_best_action():
        ''' Interface method '''

    @abc.abstractmethod
    def update():
        ''' Interface method '''

    @abc.abstractmethod
    def decay():
        ''' Interface method '''

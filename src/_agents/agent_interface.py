import abc


class IAgent(metaclass=abc.ABCMeta):

    @abc.abstractstaticmethod
    def get_best_action():
        ''' Interface method '''

    @abc.abstractstaticmethod
    def update():
        ''' Interface method '''

    @abc.abstractstaticmethod
    def decay():
        ''' Interface method '''

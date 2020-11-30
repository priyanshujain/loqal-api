import abc


class ServiceBase(metaclass=abc.ABCMeta):
    errors = {}

    @abc.abstractmethod
    def execute(self):
        pass

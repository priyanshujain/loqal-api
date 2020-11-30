from abc import ABCMeta, abstractmethod


class AbstractBaseClient(object, metaclass=ABCMeta):
    @abstractmethod
    def get_quote(self, code):
        """
        :param code: a stock code
        :return: a dictionary which contain detailed stock code.
        """
        raise NotImplementedError

import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item):
        raise NotImplementedError

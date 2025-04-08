from abc import abstractmethod, ABC


class Convertable(ABC):

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError


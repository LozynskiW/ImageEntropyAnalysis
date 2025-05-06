from abc import abstractmethod, ABC

from image_processing.models.image import ArrayImage

from typing import TypeVar, Generic, Self

class Convertable(ABC):

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError


class ProcessingResult(Convertable, ABC):

    @abstractmethod
    def calculate(self, img: ArrayImage):
        raise NotImplementedError


T = TypeVar('T')


class Calculateable(Generic[T]):
    value: T = None

    def __init__(self, *args):
        self.value = self.calculate(*args)

    @abstractmethod
    def calculate(self, *args) -> T:
        raise NotImplementedError

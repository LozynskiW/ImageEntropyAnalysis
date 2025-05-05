from abc import abstractmethod, ABC

from image_processing.models.image import ArrayImage

from typing import TypeVar, Generic

class Convertable(ABC):

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError


class ProcessingResult(Convertable, ABC):

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def calculate(self, img: ArrayImage):
        raise NotImplementedError


T = TypeVar('T')


class Calculateable(Generic[T]):
    value: T = None

    def __init__(self, **kwargs):
        self.value = self.calculate(**kwargs)

    @abstractmethod
    def calculate(self, **kwargs) -> T:
        raise NotImplementedError

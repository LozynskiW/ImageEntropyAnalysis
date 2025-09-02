from abc import abstractmethod
from image_processing.models.image import ArrayImage


class PostProcessingAlgorithm:

    def __init__(self, max_fill_factor, verbose_mode=False, show_image_after_processing=False):
        self.__max_fill_factor = max_fill_factor

    @property
    def max_fill_factor(self):
        return self.__max_fill_factor

    @max_fill_factor.setter
    def max_fill_factor(self, max_fill_factor):
        self.__max_fill_factor = max_fill_factor

    @abstractmethod
    def validate_or_process(self, img: ArrayImage, fill_factor):
        pass

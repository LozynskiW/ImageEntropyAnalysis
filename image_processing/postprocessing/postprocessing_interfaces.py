from abc import abstractmethod
from image_processing.interfaces import show_img_before_and_after_with_verbose_mode


class base(show_img_before_and_after_with_verbose_mode):

    def __init__(self, max_fill_factor, verbose_mode=False, show_image_after_processing=False):
        super().__init__(verbose_mode, show_image_after_processing)
        self.__max_fill_factor = max_fill_factor

    @property
    def max_fill_factor(self):
        return self.__max_fill_factor

    @max_fill_factor.setter
    def max_fill_factor(self, max_fill_factor):
        self.__max_fill_factor = max_fill_factor

    @abstractmethod
    def validate_or_process(self, img, fill_factor):
        pass

from abc import abstractmethod, ABC
from image_processing.interfaces import show_img_before_and_after_with_verbose_mode


class base(show_img_before_and_after_with_verbose_mode):

    @abstractmethod
    def segmentation(self, img):
        raise NotImplementedError


class threshold(base, ABC):

    def __init__(self, min_luminance_threshold, verbose_mode, show_image_after_processing):
        self.__min_luminance_threshold = min_luminance_threshold

        super().__init__(
            verbose_mode=verbose_mode,
            show_image_after_processing=show_image_after_processing
        )

    def get_min_luminance_threshold(self):
        return self.__min_luminance_threshold

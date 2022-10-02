from abc import abstractmethod
from app.image_processing.interfaces import show_img_before_and_after_with_verbose_mode


class base(show_img_before_and_after_with_verbose_mode):

    @abstractmethod
    def search_for_target(self, segmented_img):
        raise NotImplementedError

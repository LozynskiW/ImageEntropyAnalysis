from abc import abstractmethod
from app.image_processing.interfaces import verbose_mode


class base(verbose_mode):

    def __init__(self, verbose_mode):
        super().__init__(verbose_mode)

    @abstractmethod
    def process_img(self, img):
        pass

from abc import abstractmethod


class ImagePreprocessor:

    @abstractmethod
    def process_img(self, img):
        pass

from abc import abstractmethod


class ImageSegmentationAlgorithm:

    @abstractmethod
    def segmentation(self, img):
        raise NotImplementedError


class ThresholdImageSegmentationAlgorithm:

    def __init__(self, min_luminance_threshold, verbose_mode, show_image_after_processing):
        self.__min_luminance_threshold = min_luminance_threshold

    def get_min_luminance_threshold(self):
        return self.__min_luminance_threshold

from abc import abstractmethod
from image_processing.models.image import ArrayImage


class TargetDetectionAlgorithm:

    @abstractmethod
    def search_for_target(self, segmented_img: ArrayImage):
        raise NotImplementedError

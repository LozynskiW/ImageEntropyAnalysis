import copy

from image_processing.segmentation.segmentation_interfaces import ImageSegmentationAlgorithm


class NoImageProcessing(ImageSegmentationAlgorithm):

    def __init__(self):
        super().__init__(verbose_mode=False, show_image_after_processing=False)

    def segmentation(self, img):
        return copy.deepcopy(img)

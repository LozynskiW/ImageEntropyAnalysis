import copy

from image_processing.segmentation.segmentation_interfaces import ImageSegmentationAlgorithm


class NoImageProcessing(ImageSegmentationAlgorithm):

    def __init__(self):
        pass

    def segmentation(self, img):
        return copy.deepcopy(img)

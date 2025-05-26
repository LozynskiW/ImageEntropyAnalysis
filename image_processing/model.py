from dataclasses import dataclass

from image_processing.preproocessing.preprocessing_interfaces import ImagePreprocessor
from image_processing.segmentation.segmentation_interfaces import ImageSegmentationAlgorithm
from image_processing.validation.validation_interfaces import ImageValidator


@dataclass(kw_only=True, frozen=True)
class ImageSegmentationSystemConfig:
    image_preprocessors: list[ImagePreprocessor]
    img_validators: list[ImageValidator]
    image_segmentation_algorithm: ImageSegmentationAlgorithm

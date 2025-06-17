from dataclasses import dataclass
from enum import StrEnum

from image_processing.postprocessing.postprocessing_interfaces import PostProcessingAlgorithm
from image_processing.preproocessing.preprocessing_interfaces import ImagePreprocessor
from image_processing.segmentation.segmentation_interfaces import ImageSegmentationAlgorithm
from image_processing.targetdetection.targetdetection_interfaces import TargetDetectionAlgorithm
from image_processing.targetdetectionvalidation.target_detection_validation_interfaces import TargetDetectionValidator
from image_processing.targetestablishing.target_establishing_interfaces import TargetEstablishingAlgorithm
from image_processing.validation.validation_interfaces import ImageValidator


@dataclass(kw_only=True, frozen=True)
class ImageSegmentationSystemConfig:
    image_preprocessors: list[ImagePreprocessor]
    img_validators: list[ImageValidator]
    image_segmentation_algorithm: ImageSegmentationAlgorithm


@dataclass(kw_only=True, frozen=True)
class TargetDetectionSystemConfig:
    initial_validation_and_postprocessing_tools: list[PostProcessingAlgorithm]
    target_detection_algorithms: list[TargetDetectionAlgorithm]
    target_establishing: TargetEstablishingAlgorithm
    target_detection_validators: list[TargetDetectionValidator]


class Profile(StrEnum):
    SILENT = 'silent'
    VERBOSE = 'verbose'
    SHOW_IMAGE = 'show_image'
    VERBOSE_AND_SHOW_IMAGE = 'verbose_and_show_image'

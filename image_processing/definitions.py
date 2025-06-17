from abc import abstractmethod
from copy import deepcopy
from typing import overload

from image_processing._decorators import Profile, before_function
from image_processing.model import ImageSegmentationSystemConfig, TargetDetectionSystemConfig
from image_processing.models.image import ArrayImage
from image_processing.processing_results.application_actions import ProcessingAudit
from image_processing.processing_results.processing_results_facade import ProcessingResults
from image_processing.processing_results.statistical_results import StatisticalResults, EntropyMeasures


class ImageSegmentationSystem:

    def __init__(self, config: ImageSegmentationSystemConfig, profile: Profile = Profile.SILENT):
        self.__config = config
        self.__profile = profile

    def process_image(self, img: ArrayImage) -> ProcessingResults:

        img_processing_outcome = ProcessingResults()

        self.__calculate_parameters_for_given_image(img, img_processing_outcome)

        img_preprocessed = self.__preprocessing(img=img)

        if not self.__image_validation(img=img_preprocessed):
            img_processing_outcome.add_operations_audit_data(self.__results_for_invalid_img())
            return img_processing_outcome

        img_segmented = self.__segmentation(img=img_preprocessed)

        self.__calculate_parameters_after_processing(img_segmented, img_processing_outcome)

        return img_processing_outcome

    @before_function
    def __preprocessing(self, img: ArrayImage) -> ArrayImage:

        img_copy = deepcopy(img)

        for image_preprocessing_tool in self.__config.image_preprocessors:
            img_copy = image_preprocessing_tool.process_img(img_copy)

        return img_copy

    @before_function
    def __image_validation(self, img: ArrayImage) -> bool:

        img_copy = deepcopy(img)

        for img_validator in self.__config.img_validators:

            if not img_validator.validate(img_copy):
                return False

        return True

    @before_function
    def __segmentation(self, img: ArrayImage) -> ArrayImage:
        return self.__config.image_segmentation_algorithm.segmentation(deepcopy(img))

    @staticmethod
    def __results_for_invalid_img() -> ProcessingAudit:
        return ProcessingAudit(
            was_positively_validated=False,
            was_processed=None,
            was_target_detected=None
        )

    @staticmethod
    def __calculate_parameters_for_given_image(img: ArrayImage, img_processing_outcome: ProcessingResults):
        img_processing_outcome.add_statistical_parameters_before_processing(StatisticalResults.from_image(img))
        img_processing_outcome.add_entropy_measures_before_processing(EntropyMeasures.from_image(img))

    @staticmethod
    def __calculate_parameters_after_processing(img: ArrayImage, img_processing_outcome: ProcessingResults):
        img_processing_outcome.add_statistical_parameters_after_processing(StatisticalResults.from_image(img))
        img_processing_outcome.add_entropy_measures_after_processing(EntropyMeasures.from_image(img))


class ConfigurableImageSegmentationSystem:
    def __init__(self, config: ImageSegmentationSystemConfig):
        self.__config = config

    @abstractmethod
    @overload
    def process_image(self, img: ArrayImage) -> ProcessingResults:
        raise NotImplementedError

    @overload
    def process_image(self, img: ArrayImage, before_processing_func=None,
                      after_processing_func=None) -> ProcessingResults:

        if before_processing_func is not None:
            before_processing_func()

        processing_results = self.process_image(img)

        if after_processing_func is not None:
            after_processing_func()

        return processing_results


class TargetDetectionSystem:

    def __init__(self,
                 image_segmentation_system: ConfigurableImageSegmentationSystem,
                 config: TargetDetectionSystemConfig):
        self.image_segmentation_system = image_segmentation_system
        self.__config = config

    @abstractmethod
    def search_for_target(self, img: ArrayImage, verbose_mode=False, show_images=False):
        raise NotImplementedError

from image_processing.image_processing_main import ImageTargetDetectionSystem
from image_processing.preproocessing import format_standardization
from image_processing.segmentation import threshold
from image_processing.targetdetection import meanshift
from image_processing.targetestablishing import target_distance_based
from image_processing.processing_results.statistical_results import StatisticalResults, EntropyMeasures

global_verbose_mode = False

_img_preprocessing = [
    format_standardization.to_unit8_rgb(verbose_mode=global_verbose_mode)
]

_img_validators = []

_img_segment_algorithms = [
    threshold.simple_luminance_threshold(verbose_mode=global_verbose_mode,
                                         show_image_after_processing=global_verbose_mode,
                                         min_luminance_threshold=80),
]

_segmentation_fusion_method = None

_initial_validation_and_postprocessing_tools = []

_target_detection_algorithms = [
    meanshift.highest_luminance_density(verbose_mode=global_verbose_mode, show_image_after_processing=global_verbose_mode)
]

_target_establishing = [
    target_distance_based.max_target_coordinates_distance(max_variety=0.3, verbose_mode=global_verbose_mode)
]

additional_postprocessing_image_parameters = ['histogram', 'entropy', 'expected_value', 'variance']

luminance_threshold_based_system = ImageTargetDetectionSystem(
    preprocessing_tools=_img_preprocessing,
    img_validators=_img_validators,
    image_segmentation_algorithms=_img_segment_algorithms,
    segmentation_fusion_method=_segmentation_fusion_method,
    initial_validation_and_postprocessing_tools=_initial_validation_and_postprocessing_tools,
    target_detection_algorithms=_target_detection_algorithms,
    target_establishing=_target_establishing,
    additional_postprocessing_image_parameters=additional_postprocessing_image_parameters
)

additional_postprocessing_image_parameters = [StatisticalResults, EntropyMeasures]

luminance_threshold_based_system_no_target_detection = ImageTargetDetectionSystem(
    preprocessing_tools=_img_preprocessing,
    img_validators=_img_validators,
    image_segmentation_algorithms=_img_segment_algorithms,
    segmentation_fusion_method=_segmentation_fusion_method,
    initial_validation_and_postprocessing_tools=_initial_validation_and_postprocessing_tools,
    target_detection_algorithms=[],
    target_establishing=[],
    additional_postprocessing_image_parameters=additional_postprocessing_image_parameters
)
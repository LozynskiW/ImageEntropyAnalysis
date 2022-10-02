from app.image_processing.Main import ImageTargetDetectionSystem
from app.image_processing.preproocessing import format_standardization
from app.image_processing.segmentation import threshold
from app.image_processing.targetdetection import meanshift
from app.image_processing.targetestablishing import target_distance_based

global_verbose_mode = False

img_preprocessing = [
    format_standardization.to_unit8_rgb(verbose_mode=global_verbose_mode)
]

img_validators = []

img_segment_algorithms = [
    threshold.simple_luminance_threshold(verbose_mode=global_verbose_mode,
                                         show_image_after_processing=global_verbose_mode,
                                         min_luminance_threshold=80),
]

segmentation_fusion_method = None

initial_validation_and_postprocessing_tools = []

target_detection_algorithms = [
    meanshift.highest_luminance_density(verbose_mode=global_verbose_mode, show_image_after_processing=global_verbose_mode)
]

target_establishing = [
    target_distance_based.max_target_coordinates_distance(max_variety=0.3, verbose_mode=global_verbose_mode)
]

luminance_threshold_based_system = ImageTargetDetectionSystem(
    preprocessing_tools=img_preprocessing,
    img_validators=img_validators,
    image_segmentation_algorithms=img_segment_algorithms,
    segmentation_fusion_method=segmentation_fusion_method,
    initial_validation_and_postprocessing_tools=initial_validation_and_postprocessing_tools,
    target_detection_algorithms=target_detection_algorithms,
    target_establishing=target_establishing,
    additional_postprocessing_image_parameters=['histogram', 'entropy', 'expected_value', 'variance']
)

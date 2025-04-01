from image_processing.image_processing_main import ImageTargetDetectionSystem
from image_processing.validation import image_luminance
from image_processing.segmentation import contour

global_verbose_mode = False

_img_preprocessing = None

_img_validators = [
    image_luminance.maximal_mean_luminance(
        validating_mean=100,
        validating_std=50,
        deviation_from_mean_in_std=1,
        verbose_mode=global_verbose_mode),
]

_img_segment_algorithms = [
    contour.canny(verbose_mode=global_verbose_mode, show_image_after_processing=global_verbose_mode)
]

_segmentation_fusion_method = None

_initial_validation_and_postprocessing_tools = None

_target_detection_algorithms = None

_target_establishing = None

additional_postprocessing_image_parameters = ['entropy', 'expected_value', 'variance']

contour_based_system = ImageTargetDetectionSystem(
    preprocessing_tools=_img_preprocessing,
    img_validators=_img_validators,
    image_segmentation_algorithms=_img_segment_algorithms,
    segmentation_fusion_method=_segmentation_fusion_method,
    initial_validation_and_postprocessing_tools=_initial_validation_and_postprocessing_tools,
    target_detection_algorithms=_target_detection_algorithms,
    target_establishing=_target_establishing,
    additional_postprocessing_image_parameters=additional_postprocessing_image_parameters
)

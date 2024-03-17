from image_processing.image_processing_main import ImageTargetDetectionSystem
from image_processing.validation import image_luminance
from image_processing.preproocessing import vignetting
from image_processing.preproocessing import format_standardization
from image_processing.segmentation import threshold, contour
from image_processing.imagefusion import image_merging
from image_processing.postprocessing import pixel_outside_center_removal
from image_processing.targetdetection import meanshift
from image_processing.targetestablishing import target_distance_based

global_verbose_mode = False

_img_preprocessing = [
    format_standardization.to_unit8_rgb(verbose_mode=global_verbose_mode),
    vignetting.validation_correction(verbose_mode=global_verbose_mode)
]

_img_validators = [
    image_luminance.maximal_mean_luminance(
        validating_mean=100,
        validating_std=50,
        deviation_from_mean_in_std=1,
        verbose_mode=global_verbose_mode),
]

_img_segment_algorithms = [
    threshold.information_threshold(verbose_mode=global_verbose_mode, show_image_after_processing=global_verbose_mode),
    contour.canny(verbose_mode=global_verbose_mode, show_image_after_processing=global_verbose_mode)
]

_segmentation_fusion_method = image_merging.add(verbose_mode=global_verbose_mode, show_image_after_processing=global_verbose_mode)

_initial_validation_and_postprocessing_tools = [
    pixel_outside_center_removal.fill_factor_based(
        max_fill_factor=0.4,
        verbose_mode=global_verbose_mode,
        show_image_after_processing=global_verbose_mode)
]

_target_detection_algorithms = [
    meanshift.highest_luminance_density(verbose_mode=global_verbose_mode, show_image_after_processing=global_verbose_mode)
]

_target_establishing = [
    target_distance_based.max_target_coordinates_distance(max_variety=0.3, verbose_mode=global_verbose_mode)
]

additional_postprocessing_image_parameters = ['entropy', 'expected_value', 'variance']

information_entropy_based_system = ImageTargetDetectionSystem(
    preprocessing_tools=_img_preprocessing,
    img_validators=_img_validators,
    image_segmentation_algorithms=_img_segment_algorithms,
    segmentation_fusion_method=_segmentation_fusion_method,
    initial_validation_and_postprocessing_tools=_initial_validation_and_postprocessing_tools,
    target_detection_algorithms=_target_detection_algorithms,
    target_establishing=_target_establishing,
    additional_postprocessing_image_parameters=additional_postprocessing_image_parameters
)

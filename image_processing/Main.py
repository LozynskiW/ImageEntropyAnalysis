from InformationGainAnalysis.image_processing.validation import image_luminance
from InformationGainAnalysis.image_processing.preproocessing import vignetting
from InformationGainAnalysis.image_processing.preproocessing import format_standardization
from InformationGainAnalysis.image_processing.segmentation import threshold, contour
from InformationGainAnalysis.image_processing.imagefusion import image_merging
from InformationGainAnalysis.image_processing.postprocessing import pixel_outside_center_removal
from InformationGainAnalysis.image_processing.targetdetection import meanshift
from InformationGainAnalysis.image_processing.targetestablishing import target_distance_based
from copy import deepcopy


class ImageTargetDetectionSystem:
    """
        Searches for target coordinates on image based on algorithms and tools provided in parameters

        Parameters
        ----------
        img_validators : ImageValidation
            Checks if image is suitable for further processing based on specified criteria if not then image is not
            further analysed
        preprocessing_tools : ImagePreprocessing
            Processes image in order to enhance it's quality before further segmentation
        image_segmentation_algorithms : ImageSegmentation
            Algorithms to divide image into target and background pixels. More than one may be selected, but
            segmentation_fusion_method must also be used
        segmentation_fusion_method : SegmentationFusion
            Method of fusing segmentation output images into one based on some criteria if user decided
            to use more than one image segmentation algorithm
        initial_validation_and_postprocessing_tools : InitialValidationAndPostprocessing
            Validation or image processing (or both) after segmentation in order to make target detection easier or
            determine that target detection is going to be impossible and stop further calculations
        target_detection_algorithms : TargetDetectionAlgorithms
            Just as written, each algorithm (may be more than one) outputs target coordinates and area covering
            all target pixels
        target_establishing : TargetEstablishing
            Establishes target coordinates in case user used more than one target detection
            algorithm
        target_detection_validators : TargetDetectionAlgorithms
            Determines if detected target is target or not

        Raises
        ------
        ValueError
            If main_folder is blank
        ValueError
            If object is blank
        ValueError
            If dataset is blank
        ValueError
            If img_file_name is blank

        Returns
        Target coordinates in a form of [target_x_position, target_y_position, window_height, window_width]

        x,y                           window_width
        +----------------------------+
        |0000000000000000000000000000|
        |0000000000000000000000000000|
        |0000000000000000000000000000|
        |0000000000000100000000000000|
        |0000000011111111110000000000|
        |0000000000010100000000000000|
        |0000000000100100000000000000|
        |0000000000000000000000000000|
        +----------------------------+ window_height

        """

    def __init__(self,
                 img_validators=None,
                 preprocessing_tools=None,
                 image_segmentation_algorithms=None,
                 segmentation_fusion_method=None,
                 initial_validation_and_postprocessing_tools=None,
                 target_detection_algorithms=None,
                 target_establishing=None,
                 target_detection_validators=None,
                 ):

        if preprocessing_tools is None:
            preprocessing_tools = []
        if img_validators is None:
            img_validators = []
        if image_segmentation_algorithms is None:
            image_segmentation_algorithms = []
        if target_detection_algorithms is None:
            target_detection_algorithms = []
        if initial_validation_and_postprocessing_tools is None:
            initial_validation_and_postprocessing_tools = []
        if target_establishing is None:
            target_establishing = []
        if target_detection_validators is None:
            target_detection_validators = []

        self.__preprocessing_tools = preprocessing_tools
        self.__img_validators = img_validators
        self.__image_segmentation_algorithms = image_segmentation_algorithms
        self.__segmentation_fusion_method = segmentation_fusion_method
        self.__initial_validation_and_postprocessing_tools = initial_validation_and_postprocessing_tools
        self.__target_detection_algorithms = target_detection_algorithms
        self.__target_establishing = target_establishing
        self.__target_detection_validators = target_detection_validators

    def search_for_target(self, img, verbose_mode=False):

        img_processing_outcome = {
            "original_img": img,
            "processed_img": None,
            "is_valid": False,
            "was_processed": False,
            "fill_factor": 0,
            "is_target_detected": False,
            "target_coordinates": []
        }

        # PREPROCESSING

        img = self.__preprocessing(img=img, verbose_mode=verbose_mode)

        # IMAGE VALIDATION

        if not self.__image_validation(img=img, verbose_mode=verbose_mode):
            return img_processing_outcome

        img_processing_outcome["is_valid"] = True

        # SEGMENTATION

        imgs_segmented = self.__segmentation(img=img, verbose_mode=verbose_mode)

        # SEGMENTATION FUSION

        img_segmented, fill_factor = self.__segmentation_fusion(imgs_segmented=imgs_segmented, verbose_mode=verbose_mode)

        img_processing_outcome["was_processed"] = True

        # INITIAL VALIDATION AND POSTPROCESSING

        outcome, img_segmented = self.__initial_validation_and_postprocessing(img_segmented=img_segmented,
                                                                              fill_factor=fill_factor,
                                                                              verbose_mode=verbose_mode)

        img_processing_outcome["processed_img"] = img_segmented
        img_processing_outcome["fill_factor"] = fill_factor

        if not outcome:
            return img_processing_outcome

        # TARGET DETECTION

        target_coordinates = self.__detect_target(img_segmented=img_segmented, verbose_mode=verbose_mode)

        # TARGET ESTABLISHING

        target_location = self.__establish_target(target_coordinates=target_coordinates, verbose_mode=verbose_mode)

        # TARGET DETECTION VALIDATION

        if not self.__validate_target(target_coordinates=target_location, verbose_mode=verbose_mode):
            return  img_processing_outcome

        img_processing_outcome["is_target_detected"] = True
        img_processing_outcome["target_coordinates"] = target_location

        return img_processing_outcome

    def __preprocessing(self, img, verbose_mode):

        img = deepcopy(img)

        for image_preprocessing_tool in self.__preprocessing_tools:
            if verbose_mode: print("Preprocessing via:", str(image_preprocessing_tool))

            img = image_preprocessing_tool.process_img(img)

        if verbose_mode:
            print("Preprocessing done")
            print()
        return img

    def __image_validation(self, img, verbose_mode):
        img = deepcopy(img)

        if verbose_mode: print("Initiating image validation")

        for img_validator in self.__img_validators:

            if verbose_mode: print("Validating via:", str(img_validator))

            if not img_validator.validate(img):
                if verbose_mode: print("Image validation done...image NOT valid")
                return False

        if verbose_mode:
            print("Image validation done...image valid")
            print()

        return True

    def __segmentation(self, img, verbose_mode):

        img = deepcopy(img)

        imgs_segmented = []
        for img_segmentation_algorithm in self.__image_segmentation_algorithms:

            if verbose_mode: print("segmentation via:", str(img_segmentation_algorithm))

            segmented_img = img_segmentation_algorithm.segmentation(img)
            imgs_segmented.append(segmented_img)

        if verbose_mode:
            print("Image segmentation done")
            print()
        return imgs_segmented

    def __segmentation_fusion(self, imgs_segmented, verbose_mode):

        imgs_segmented = deepcopy(imgs_segmented)

        if verbose_mode: print("Fusing segmented images via:", str(self.__segmentation_fusion_method))

        img_segmented, fill_factor = self.__segmentation_fusion_method.fuse(imgs_segmented)

        if verbose_mode:
            print("DONE")
            print()

        return img_segmented, fill_factor

    def __initial_validation_and_postprocessing(self, img_segmented, fill_factor, verbose_mode):

        img_segmented = deepcopy(img_segmented)

        for i in range(0, len(self.__initial_validation_and_postprocessing_tools)):
            initial_validation_and_postprocessing_tool = self.__initial_validation_and_postprocessing_tools[i]

            if verbose_mode: print("Initial validation and postprocessing via:",
                                   str(initial_validation_and_postprocessing_tool))

            outcome, img_segmented, fill_factor = initial_validation_and_postprocessing_tool.validate_or_process(
                img_segmented, fill_factor)

            if not outcome:
                print('image segmentation not enough to detect target')
                print()
                return False, img_segmented

        if verbose_mode:
            print("Initial validation and postprocessing done")
            print()

        return True, img_segmented

    def __detect_target(self, img_segmented, verbose_mode):

        img_segmented = deepcopy(img_segmented)

        target_coordinates = []

        for i in range(0, len(self.__target_detection_algorithms)):
            target_detection_algorithm = self.__target_detection_algorithms[i]

            if verbose_mode: print("Searching for target via:", str(target_detection_algorithm))
            target_coordinates.append(target_detection_algorithm.search_for_target(img_segmented))

        if verbose_mode:
            print("Target detection done")
            print(target_coordinates)
            print()

        return target_coordinates

    def __establish_target(self, target_coordinates, verbose_mode):

        if verbose_mode: print("Searching for target via:", str(self.__target_establishing[0]))

        target_location = self.__target_establishing[0].establish_target_location(target_coordinates)

        if verbose_mode:
            if target_location:
                print("Target is at: ", target_location)
            else:
                print("Target undetected")
            print()

        return target_location

    def __validate_target(self, target_coordinates, verbose_mode):

        for target_detection_validator in self.__target_detection_validators:

            if verbose_mode: print("Validating target detection via:", str(target_detection_validator))

            if not target_detection_validator.validate(target_coordinates):
                if verbose_mode: print("Detected target does not match given criteria, target undetected")
                return False

        if verbose_mode: print("Detected target matches given criteria, target detected")

        return True

"""
EXAMPLE USAGE

from skimage import io

img_preprocessing = [
    format_standardization.to_unit8_rgb(verbose_mode=True),
    vignetting.validation_correction(verbose_mode=True)
]

img_validators = [
    image_luminance.maximal_mean_luminance(
        validating_mean=100,
        validating_std=50,
        deviation_from_mean_in_std=1,
        verbose_mode=True),
]

img_segment_algorithms = [
    threshold.information_threshold(verbose_mode=True, show_image_after_processing=True),
    contour.canny(verbose_mode=True, show_image_after_processing=True)
]

segmentation_fusion_method = image_merging.add(verbose_mode=True, show_image_after_processing=True)

initial_validation_and_postprocessing_tools = [
    pixel_outside_center_removal.fill_factor_based(
        max_fill_factor=0.2,
        verbose_mode=True,
        show_image_after_processing=True)
]

target_detection_algorithms = [
    meanshift.highest_luminance_density(verbose_mode=True, show_image_after_processing=True)
]

target_establishing = [
    target_distance_based.max_target_coordinates_distance(max_variety=0.3, verbose_mode=True)
]

test = ImageTargetDetectionSystem(preprocessing_tools=img_preprocessing,
                                  img_validators=img_validators,
                                  image_segmentation_algorithms=img_segment_algorithms,
                                  segmentation_fusion_method=segmentation_fusion_method,
                                  initial_validation_and_postprocessing_tools=initial_validation_and_postprocessing_tools,
                                  target_detection_algorithms=target_detection_algorithms,
                                  target_establishing=target_establishing
                                  )

img = io.imread('D:/magisterka/antrax/sarna/2021-02-04T211617/2021 02 04 21 16 17 812.tif')

test.search_for_target(img=img, verbose_mode=True)

"""
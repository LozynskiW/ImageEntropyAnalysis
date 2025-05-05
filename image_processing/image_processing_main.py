from image_processing.basictools.utilities import show_image, calculate_fill_factor, show_detected_target_on_img
from image_processing.basictools import statisticalparameters
from copy import deepcopy

from image_processing.processing_results.application_actions import ProcessingAudit
from image_processing.processing_results.processing_results_facade import ProcessingResults
from image_processing.processing_results.processing_results_interfaces import ProcessingResult
from image_processing.processing_results.statistical_results import StatisticalResults, EntropyMeasures
from image_processing.models.image import ArrayImage


class ImageTargetDetectionSystem:
    """
        Searches for target coordinates on image based on algorithms and tools provided in parameters, see docs

        Raises
        ------
        ValueError
            If main_folder is blank
            If object is blank
            If dataset is blank
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
                 additional_postprocessing_image_parameters=None
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
        if additional_postprocessing_image_parameters is None:
            additional_postprocessing_image_parameters = []

        self.__preprocessing_tools = preprocessing_tools
        self.__img_validators = img_validators
        self.__image_segmentation_algorithms = image_segmentation_algorithms
        self.__segmentation_fusion_method = segmentation_fusion_method
        self.__initial_validation_and_postprocessing_tools = initial_validation_and_postprocessing_tools
        self.__target_detection_algorithms = target_detection_algorithms
        self.__target_establishing = target_establishing
        self.__target_detection_validators = target_detection_validators
        self.__additional_postprocessing_image_parameters = additional_postprocessing_image_parameters

    def process_image(self, img: ArrayImage) -> ProcessingResults:

        img_processing_outcome = ProcessingResults()
        stat_res = StatisticalResults()
        stat_res.calculate(img)
        img_processing_outcome.add_statistical_parameters_before_processing(stat_res)
        show_image(img=img, fig_title="Given image - before any processing")

        img_preprocessed = self.__preprocessing(img=img)

        show_image(img=img_preprocessed, fig_title="Image after preprocessing")

        if not self.__image_validation(img=img_preprocessed):
            img_processing_outcome.add_operations_audit_data(
                ProcessingAudit(
                    was_positively_validated=False,
                    was_processed=False,
                    was_target_detected=False
                )
            )
            return img_processing_outcome

        imgs_segmented = self.__segmentation(img=img_preprocessed)

        if self.__segmentation_fusion_method:
            img_segmented, fill_factor = self.__segmentation_fusion(imgs_segmented=imgs_segmented)

        else:
            img_segmented = imgs_segmented[0]
            fill_factor = calculate_fill_factor(img=img_segmented)

        show_image(img=img_segmented, fig_title="Image after segmentation")

        stat_res.calculate(img_segmented)
        img_processing_outcome.add_statistical_parameters_after_processing(stat_res)

        return img_processing_outcome


    def search_for_target(self, img: ArrayImage, verbose_mode=False, show_images=False):

        img_processing_outcome = ProcessingResults()

        if show_images:
            show_image(img=img, fig_title="Original image")

        # PREPROCESSING

        img = self.__preprocessing(img=img, verbose_mode=verbose_mode)

        if show_images:
            show_image(img=img, fig_title="Image after preprocessing")

        # IMAGE VALIDATION

        if not self.__image_validation(img=img, verbose_mode=verbose_mode):
            img_processing_outcome.add_operations_audit_data(
                ProcessingAudit(
                    was_positively_validated=False,
                    was_processed=False,
                    was_target_detected=False
                )
            )
            return img_processing_outcome.to_dict()

        # SEGMENTATION

        imgs_segmented = self.__segmentation(img=img, verbose_mode=verbose_mode)

        # SEGMENTATION FUSION

        if self.__segmentation_fusion_method:

            img_segmented, fill_factor = self.__segmentation_fusion(imgs_segmented=imgs_segmented,
                                                                    verbose_mode=verbose_mode)

        else:

            img_segmented = imgs_segmented[0]
            fill_factor = calculate_fill_factor(img=img_segmented)

        if show_images:
            show_image(img=img_segmented, fig_title="Image after segmentation fusion")

        # INITIAL VALIDATION AND POSTPROCESSING

        if self.__initial_validation_and_postprocessing_tools:

            outcome, img_segmented, fill_factor = self.__initial_validation_and_postprocessing(img_segmented=img_segmented,
                                                                                               fill_factor=fill_factor,
                                                                                               verbose_mode=verbose_mode)

            if show_images:
                show_image(img=img_segmented, fig_title="Image after initial validation and postprocessing")

            if not outcome:
                img_processing_outcome.add_operations_audit_data(
                    ProcessingAudit(
                        was_positively_validated=True,
                        was_processed=True,
                        was_target_detected=False
                    )
                )
                return img_processing_outcome.to_dict()

        img_processing_outcome["fill_factor"] = float(fill_factor)

        # TARGET DETECTION

        target_coordinates = self.__detect_target(img_segmented=img_segmented, verbose_mode=verbose_mode)

        # TARGET ESTABLISHING

        target_location = self.__establish_target(target_coordinates=target_coordinates, verbose_mode=verbose_mode)

        if show_images:

            show_detected_target_on_img(img=img_segmented,
                                    target_x=target_coordinates[0][0],
                                    target_y=target_coordinates[0][1],
                                    window_height=10,
                                    window_width=10)

        # TARGET DETECTION VALIDATION

        if not self.__validate_target(target_coordinates=target_location, verbose_mode=verbose_mode):
            img_processing_outcome.add_operations_audit_data(
                    ProcessingAudit(
                        was_positively_validated=True,
                        was_processed=True,
                        was_target_detected=False
                    )
                )
            return img_processing_outcome.to_dict()

        img_processing_outcome["is_target_detected"] = True
        img_processing_outcome["target_coordinates"] = target_location

        additional_postprocessing_parameters = self.__calculate_additional_postprocessing_parameters(img,
                                                                                                     additional_parameters=self.__additional_postprocessing_image_parameters,
                                                                                                     is_image_processed=False)
        for key in additional_postprocessing_parameters:
            img_processing_outcome[key] = additional_postprocessing_parameters[key]

        additional_postprocessing_parameters = self.__calculate_additional_postprocessing_parameters(img_segmented,
                                                                                                     additional_parameters=self.__additional_postprocessing_image_parameters,
                                                                                                     is_image_processed=True)
        for key in additional_postprocessing_parameters:
            img_processing_outcome[key] = additional_postprocessing_parameters[key]

        img_processing_outcome.add_operations_audit_data(
            ProcessingAudit(
                was_positively_validated=True,
                was_processed=True,
                was_target_detected=True
            )
        )
        return img_processing_outcome.to_dict()


    def __preprocessing(self, img, verbose_mode=False):

        img = deepcopy(img)

        for image_preprocessing_tool in self.__preprocessing_tools:
            if verbose_mode: print("Preprocessing via:", str(image_preprocessing_tool))

            img = image_preprocessing_tool.process_img(img)

        if verbose_mode:
            print("Preprocessing done")
            print()
        return img

    def __image_validation(self, img, verbose_mode=False):
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

    def __segmentation(self, img, verbose_mode=False):

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

    def __segmentation_fusion(self, imgs_segmented, verbose_mode=False):

        imgs_segmented = deepcopy(imgs_segmented)

        if verbose_mode: print("Fusing segmented images via:", str(self.__segmentation_fusion_method))

        img_segmented, fill_factor = self.__segmentation_fusion_method.fuse(imgs_segmented)

        if verbose_mode:
            print("DONE")
            print()


        return img_segmented, fill_factor

    def __initial_validation_and_postprocessing(self, img_segmented, fill_factor, verbose_mode):

        img_segmented = deepcopy(img_segmented)
        new_fill_factor = fill_factor

        for i in range(0, len(self.__initial_validation_and_postprocessing_tools)):
            initial_validation_and_postprocessing_tool = self.__initial_validation_and_postprocessing_tools[i]

            if verbose_mode: print("Initial validation and postprocessing via:",
                                   str(initial_validation_and_postprocessing_tool))

            outcome, img_segmented, new_fill_factor = initial_validation_and_postprocessing_tool.validate_or_process(
                img_segmented, fill_factor)

            if not outcome:
                print('image segmentation not enough to detect target')
                print()
                return False, img_segmented, 0

        if verbose_mode:
            print("Initial validation and postprocessing done")
            print()

        return True, img_segmented, new_fill_factor

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

    @staticmethod
    def __calculate_additional_postprocessing_parameters(img, additional_parameters, is_image_processed=False):

        additional_postprocessing_parameters = {}

        name = "original"
        if is_image_processed:
            name = "processed"

        for parameter in additional_parameters:

            if parameter == 'histogram':
                grayscale, gray_shade_prob = statisticalparameters.image_histogram(im=img, normalize_to_pdf=False)
                additional_postprocessing_parameters["histogram_of_" + name + "_image"] = tuple(gray_shade_prob)

            if parameter == 'entropy':
                H, H_n = statisticalparameters.information_entropy(im=img)
                additional_postprocessing_parameters["entropy_of_" + name + "_image"] = float(H)

            if parameter == 'expected_value':
                grayscale, gray_shade_prob = statisticalparameters.image_histogram(im=img, normalize_to_pdf=True)
                additional_postprocessing_parameters["expected_value_of_" + name + "_image"] = \
                    float(statisticalparameters.exp_val_from_histogram(grayscale, gray_shade_prob))

            if parameter == 'variance':
                grayscale, gray_shade_prob = statisticalparameters.image_histogram(im=img, normalize_to_pdf=True)
                expected_val = statisticalparameters.exp_val_from_histogram(grayscale, gray_shade_prob)

                additional_postprocessing_parameters["variance_of_" + name + "_image"] = \
                    float(statisticalparameters.variance_from_histogram(grayscale, gray_shade_prob, expected_val))

        return additional_postprocessing_parameters

    @staticmethod
    def __calculate_processing_results_for_image(img: ArrayImage, processing_results_calc: tuple[ProcessingResult]):

        for res in processing_results_calc:
            res.calculate(img)

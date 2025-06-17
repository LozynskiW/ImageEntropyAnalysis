import math
from abc import ABC
from array import array
from copy import deepcopy
from typing import Self

from image_processing.basictools import statisticalparameters
from image_processing.models.image import ArrayImage
from image_processing.processing_results.processing_results_interfaces import ProcessingResult, Calculateable, T


class Histogram:
    __variable_values: array
    __variable_values_counts: array

    def __init__(self, variable_values: array, variable_values_counts: array):
        if len(variable_values) != len(variable_values_counts):
            raise ValueError("Length of variable_values does not equal variable_values_counts, histogram cannot be "
                             "created")
        self.__variable_values = variable_values
        self.__variable_values_counts = variable_values_counts

    def normalize(self) -> Self:
        histogram_copy = deepcopy(self)
        normalized_values_counts = statisticalparameters.normalize_histogram(self.get_values_counts())
        histogram_copy._set_variable_values_counts(normalized_values_counts)
        return histogram_copy

    def _set_variable_values_counts(self, variable_values_counts: array):
        self.__variable_values_counts = variable_values_counts

    def get_variables_values(self) -> array:
        return self.__variable_values

    def get_values_counts(self) -> array:
        return self.__variable_values_counts


class ImageHistogram(Histogram, ABC):

    def __init__(self, image: ArrayImage):
        super().__init__(self.calculate(image))

    def calculate(self, image: ArrayImage):
        return statisticalparameters.image_histogram(im=image, normalize_to_pdf=False)


class InformationForVariableStates(ImageHistogram):

    def calculate(self, image: ArrayImage):
        return statisticalparameters.information_for_image_histogram(image)


class EntropyForVariableStates(ImageHistogram):

    def calculate(self, image: ArrayImage):
        return statisticalparameters.information_entropy_for_image_histogram(image)


class ExpectedValue(Calculateable[float], ABC):

    def __init__(self, img: ArrayImage):
        super().__init__(img)

    def calculate(self, img: ArrayImage) -> float:
        pixel_value_sum = 0
        pixel_number = 0
        for y in range(0, len(img[0])):
            for x in range(0, len(img)):
                pixel_value_sum += img[x][y]
                pixel_number += 1
        if pixel_number == 0:
            return 0
        return float(pixel_value_sum/pixel_number)

    def __sub__(self, other) -> float:
        return self.value - other

    def __add__(self, other) -> float:
        return self.value + other


class Variance(Calculateable[float], ABC):

    def __init__(self, img: ArrayImage, expected_val: ExpectedValue):
        super().__init__(img, expected_val)

    def calculate(self, img: ArrayImage, expected_val: ExpectedValue) -> float:
        variance_sum = 0
        pixel_number = 0
        for y in range(0, len(img[0])):
            for x in range(0, len(img)):
                variance_sum += math.pow(img[x][y] - expected_val.value, 2)
                pixel_number += 1
        if pixel_number == 0:
            return 0
        return float(variance_sum / pixel_number)


class StandardDeviation(Calculateable[float], ABC):

    def __init__(self, variance: Variance):
        super().__init__(variance)

    def calculate(self, variance: Variance) -> float:
        return float(math.sqrt(variance.value))


class InformationInBits(Calculateable[float], ABC):
    def __init__(self, information_for_variable_states: InformationForVariableStates):
        super().__init__(information_for_variable_states)

    def calculate(self, information_for_variable_states: InformationForVariableStates) -> float:
        return float(sum(information_for_variable_states.get_values_counts()))


class InformationEntropyInBits(Calculateable[float], ABC):
    def __init__(self, entropy_for_variable_states: EntropyForVariableStates):
        super().__init__(entropy_for_variable_states)

    def calculate(self, entropy_for_variable_states: EntropyForVariableStates) -> float:
        return float(sum(entropy_for_variable_states.get_values_counts()))


class StatisticalResults(ProcessingResult, ABC):
    __histogram: ImageHistogram
    __histogram_normalized: ImageHistogram
    __expected_value: ExpectedValue
    __variance: Variance
    __standard_deviation: StandardDeviation

    def to_dict(self) -> dict:
        return dict([
            ("histogram", self.__histogram.get_values_counts()),
            ("histogram_normalized", self.__histogram_normalized.get_values_counts()),
            ("expected_value", self.__expected_value.value),
            ("variance", self.__variance.value),
            ("standard_deviation", self.__standard_deviation.value)
        ])

    def calculate(self, img: ArrayImage):
        self.__histogram = ImageHistogram(img)
        self.__histogram_normalized = self.__histogram.normalize()
        self.__expected_value = ExpectedValue(img=img)
        self.__variance = Variance(img=img,
                                   expected_val=self.__expected_value)
        self.__standard_deviation = StandardDeviation(self.__variance)

    @staticmethod
    def from_image(img: ArrayImage) -> ProcessingResult:
        statistical_results = StatisticalResults()
        statistical_results.calculate(img)
        return statistical_results

    def __str__(self):
        return self.to_dict()


class EntropyMeasures(ProcessingResult, ABC):
    __information_for_x: InformationForVariableStates
    __information_in_bits: InformationInBits
    __entropy_for_x: EntropyForVariableStates
    __entropy_in_bits: InformationEntropyInBits

    def to_dict(self) -> dict:
        return dict([
            ("information_for_x", self.__information_for_x.get_values_counts()),
            ("information_in_bits", self.__information_in_bits.value),
            ("entropy_for_x", self.__entropy_for_x.get_values_counts()),
            ("entropy_in_bits", self.__entropy_in_bits.value)
        ])

    def calculate(self, img: ArrayImage):
        self.__information_for_x = InformationForVariableStates(img)
        self.__information_in_bits = InformationInBits(self.__information_for_x)
        self.__entropy_for_x = EntropyForVariableStates(img)
        self.__entropy_in_bits = InformationEntropyInBits(self.__entropy_for_x)

    @staticmethod
    def from_image(img: ArrayImage) -> ProcessingResult:
        entropy_measures = EntropyMeasures()
        entropy_measures.calculate(img)
        return entropy_measures

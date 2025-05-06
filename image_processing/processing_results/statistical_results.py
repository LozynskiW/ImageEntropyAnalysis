from abc import ABC
from array import array
from copy import deepcopy
from dataclasses import dataclass
from typing import Self

from image_processing.basictools import statisticalparameters
from image_processing.models.image import ArrayImage
from image_processing.processing_results.processing_results_interfaces import ProcessingResult, Calculateable, T


class ImageHistogram:
    __variable_values: array
    __variable_values_counts: array

    def __init__(self, image: ArrayImage):
        values, values_counts = self.calculate(image)
        self.__variable_values = values
        self.__variable_values_counts = values_counts

    def calculate(self, image: ArrayImage):
        return statisticalparameters.image_histogram(im=image, normalize_to_pdf=False)

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


class InformationForVariableStates(ImageHistogram):

    def calculate(self, image: ArrayImage):
        return statisticalparameters.information_for_image_histogram(image)


class EntropyForVariableStates(ImageHistogram):

    def calculate(self, image: ArrayImage):
        return statisticalparameters.information_entropy_for_image_histogram(image)


class ExpectedValue(Calculateable[float], ABC):

    def __init__(self, grayscale: array, gray_shade_prob: array):
        super().__init__(grayscale, gray_shade_prob)

    def calculate(self, grayscale: array, gray_shade_prob: array) -> float:
        return float(statisticalparameters.exp_val_from_histogram(grayscale, gray_shade_prob))

    def __sub__(self, other) -> float:
        return self.value - other

    def __add__(self, other) -> float:
        return self.value + other


class Variance(Calculateable[float], ABC):

    def __init__(self, grayscale: array, gray_shade_prob: array, expected_val: ExpectedValue):
        super().__init__(grayscale, gray_shade_prob, expected_val.value)

    def calculate(self, grayscale: array, gray_shade_prob: array, expected_val: ExpectedValue) -> float:
        return float(statisticalparameters.variance_from_histogram(grayscale, gray_shade_prob, expected_val))


class StandardDeviation(Calculateable[float], ABC):

    def __init__(self, variance: Variance):
        super().__init__(variance)

    def calculate(self, variance: Variance) -> float:
        return float(statisticalparameters.std_dev_from_variance(variance.value))


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
        self.__expected_value = ExpectedValue(grayscale=self.__histogram_normalized.get_variables_values(),
                                              gray_shade_prob=self.__histogram_normalized.get_values_counts())
        self.__variance = Variance(grayscale=self.__histogram_normalized.get_variables_values(),
                                   gray_shade_prob=self.__histogram_normalized.get_values_counts(),
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

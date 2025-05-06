from abc import ABC
from array import array
from copy import deepcopy
from dataclasses import dataclass
from typing import Self

from image_processing.basictools import statisticalparameters
from image_processing.models.image import ArrayImage
from image_processing.processing_results.processing_results_interfaces import ProcessingResult, Calculateable


class ImageHistogram:
    __variable_values: array
    __variable_values_counts: array

    def __init__(self, image: ArrayImage):
        values, values_counts = statisticalparameters.image_histogram(im=image, normalize_to_pdf=False)
        self.__variable_values = values
        self.__variable_values_counts = values_counts

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


class StatisticalResults(ProcessingResult, ABC):
    __histogram: ImageHistogram
    __histogram_normalized: ImageHistogram
    __expected_value: ExpectedValue
    __variance: Variance

    def to_dict(self) -> dict:
        return dict([
            ("histogram", self.__histogram.get_values_counts()),
            ("histogram_normalized", self.__histogram_normalized.get_values_counts()),
            ("expected_value", self.__expected_value.value),
            ("variance", self.__variance.value)
        ])

    def calculate(self, img: ArrayImage):
        self.__histogram = ImageHistogram(img)
        self.__histogram_normalized = self.__histogram.normalize()
        self.__expected_value = ExpectedValue(grayscale=self.__histogram_normalized.get_variables_values(),
                                              gray_shade_prob=self.__histogram_normalized.get_values_counts())
        self.__variance = Variance(grayscale=self.__histogram_normalized.get_variables_values(),
                                   gray_shade_prob=self.__histogram_normalized.get_values_counts(),
                                   expected_val=self.__expected_value)

    @staticmethod
    def from_image(img: ArrayImage) -> ProcessingResult:
        statistical_results = StatisticalResults()
        statistical_results.calculate(img)
        return statistical_results

    def __str__(self):
        return self.to_dict()


@dataclass(frozen=True, init=True)
class EntropyMeasures(ProcessingResult, ABC):
    information_in_bits: float
    entropy_for_x: ImageHistogram
    entropy: float

    def to_dict(self) -> dict:
        return dict([
            ("information_in_bits", self.information_in_bits),
            ("entropy_for_x", self.entropy_for_x),
            ("entropy", self.entropy)
        ])

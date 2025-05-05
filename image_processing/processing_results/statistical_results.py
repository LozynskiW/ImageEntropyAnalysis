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


@dataclass(frozen=True, init=True, eq=True)
class StatisticalResults(ProcessingResult, ABC):
    histogram: ImageHistogram
    expected_value: float
    variance: float

    def to_dict(self) -> dict:
        return dict([
            ("histogram", self.histogram),
            ("expected_value", self.expected_value),
            ("variance", self.variance)
        ])

    def calculate(self, img: ArrayImage):
        _, histogram = statisticalparameters.image_histogram(im=img, normalize_to_pdf=False)
        grayscale, gray_shade_prob = statisticalparameters.image_histogram(im=img, normalize_to_pdf=True)
        expected_val = statisticalparameters.exp_val_from_histogram(grayscale, gray_shade_prob)
        variance = float(statisticalparameters.variance_from_histogram(grayscale, gray_shade_prob, expected_val))


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

    def get_name(self) -> str:
        return "EntropyMeasures"


class ExpectedValue(Calculateable[float], ABC):

    def calculate(self, grayscale, gray_shade_prob: ImageHistogram) -> float:
        return float(statisticalparameters.exp_val_from_histogram(grayscale, gray_shade_prob))


class Variance(Calculateable[float], ABC):

    def calculate(self, grayscale, gray_shade_prob: ImageHistogram, expected_val: ExpectedValue) -> float:
        return float(statisticalparameters.variance_from_histogram(grayscale, gray_shade_prob, expected_val))

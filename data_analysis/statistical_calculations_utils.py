import math
import statistics
from abc import ABC
from array import array

from image_processing.processing_results.processing_results_interfaces import Calculateable
from image_processing.processing_results.statistical_results import Histogram, ExpectedValue


class ExpectedValueFromHistogram(Calculateable[float], ABC):

    def __init__(self, variable_values: array, variable_values_counts: array):
        histogram = Histogram(variable_values, variable_values_counts)
        histogram_normalized = histogram.normalize()
        super().__init__(histogram_normalized.get_variables_values(), histogram_normalized.get_values_counts())

    def calculate(self, grayscale: array, gray_shade_prob: array) -> float:
        exp_val = 0

        for i in range(0, len(grayscale)):
            exp_val += grayscale[i] * gray_shade_prob[i]

        return exp_val

    def __sub__(self, other) -> float:
        return self.value - other

    def __add__(self, other) -> float:
        return self.value + other


class ExpectedValueFromValuesCounts(Calculateable[float], ABC):

    def __init__(self, variable_values_counts: array):
        super().__init__(variable_values_counts)

    def calculate(self, variable_values_counts: array) -> float:

        return statistics.fmean(_variable_values_from__values_counts(variable_values_counts))

    def __sub__(self, other) -> float:
        return self.value - other

    def __add__(self, other) -> float:
        return self.value + other


class VarianceFromValuesCounts(Calculateable[float], ABC):

    def __init__(self, variable_values_counts: array):
        super().__init__(variable_values_counts)

    def calculate(self, variable_values_counts: array) -> float:

        return statistics.variance(_variable_values_from__values_counts(variable_values_counts))


class VarianceFromHistogram(Calculateable[float], ABC):

    def __init__(self, variable_values: array, variable_values_counts: array):
        histogram = Histogram(variable_values, variable_values_counts)
        histogram_normalized = histogram.normalize()
        expected_val = ExpectedValueFromHistogram(variable_values, variable_values_counts)
        super().__init__(histogram_normalized.get_variables_values(),
                         histogram_normalized.get_values_counts(),
                         expected_val)

    def calculate(self, grayscale: array, gray_shade_prob: array, expected_val: ExpectedValue) -> float:
        variance = 0

        for i in range(0, len(grayscale)):
            variance += math.pow(grayscale[i] - expected_val.value, 2)

        return variance / len(grayscale)


def _variable_values_from__values_counts(variable_values_counts: array) -> list[float]:
    variable_values = []

    for i in range(1, len(variable_values_counts)):
        for v in range(0, int(variable_values_counts[i])):
            variable_values.append(float(i))

    return variable_values
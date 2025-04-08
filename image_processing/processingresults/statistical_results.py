from abc import ABC
from array import array
from dataclasses import dataclass

from image_processing.processingresults.processing_results_interfaces import Convertable


@dataclass(frozen=True)
class Histogram:
    grayscale: array
    probabilities: array

    @DeprecationWarning("only for legacy compliance")
    def get_x_and_p_x(self):
        return self.grayscale, self.probabilities


@dataclass(frozen=True)
class StatisticalResults(Convertable, ABC):
    histogram: Histogram
    expected_value: float
    variance: float

    def to_dict(self) -> dict:
        return dict([
            ("histogram", self.histogram),
            ("expected_value", self.expected_value),
            ("variance", self.variance)
        ])


@dataclass(frozen=True)
class EntropyMeasures(Convertable, ABC):
    information_in_bits: float
    entropy_for_x: Histogram
    entropy: float

    def to_dict(self) -> dict:
        return dict([
            ("information_in_bits", self.information_in_bits),
            ("entropy_for_x", self.entropy_for_x),
            ("entropy", self.entropy)
        ])

from abc import ABC
from dataclasses import dataclass

from image_processing.processing_results.processing_results_interfaces import ProcessingResult


@dataclass(frozen=True)
class ProcessingAudit(ProcessingResult, ABC):
    was_positively_validated: bool
    was_processed: bool
    was_target_detected: bool

    def to_dict(self) -> dict:
        return dict([
            ("was_positively_validated", self.was_positively_validated),
            ("was_processed", self.was_processed),
            ("was_target_detected", self.was_target_detected)
        ])

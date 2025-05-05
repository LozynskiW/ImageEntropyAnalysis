from abc import ABC
from dataclasses import dataclass

from image_processing.processing_results.processing_results_interfaces import ProcessingResult


@dataclass(frozen=True)
class ProcessingAudit(ProcessingResult, ABC):
    is_processable: bool
    was_processed: bool
    was_target_detected: bool

    def to_dict(self) -> dict:
        return dict([
            ("is_processable", self.is_processable),
            ("was_processed", self.was_processed),
            ("was_target_detected", self.was_target_detected)
        ])

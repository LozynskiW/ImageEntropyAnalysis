from abc import ABC
from dataclasses import dataclass

from image_processing.processingresults.processing_results_interfaces import Convertable


@dataclass(frozen=True)
class ProcessingAudit(Convertable, ABC):
    is_processable: bool
    was_processed: bool
    was_target_detected: bool

    def to_dict(self) -> dict:
        return dict([
            ("is_processable", self.is_processable),
            ("was_processed", self.was_processed),
            ("was_target_detected", self.was_target_detected)
        ])

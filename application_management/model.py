from dataclasses import dataclass


@dataclass
class DataIdentification:
    object: str
    file_name: str
    dataset: str

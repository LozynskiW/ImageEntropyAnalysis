from abc import abstractmethod

from image_data_logs_readers.models import GeoLocalizationData


class LogsReader:
    _logs = list[GeoLocalizationData]

    def __init__(self, path_to_logs_file: str):
        self._logs = self._load_logs(path_to_logs_file)

    @abstractmethod
    def _load_logs(self, path_to_file: str) -> list[GeoLocalizationData]:
        raise NotImplementedError

    @abstractmethod
    def get_log_by_image_name(self, image_name: str) -> GeoLocalizationData:
        raise NotImplementedError

    def get_logs(self) -> list[GeoLocalizationData]:
        return self._logs

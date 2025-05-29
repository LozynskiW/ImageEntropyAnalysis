import json
from abc import ABC

from image_data_logs_readers.definitions import LogsReader
from image_data_logs_readers.models import GeoLocalizationData


class JsonLogsReader(LogsReader, ABC):

    def _load_logs(self, path_to_file: str) -> list[GeoLocalizationData]:
        gps_data_list: list[GeoLocalizationData] = []

        with open(path_to_file) as f:
            logs_map = json.load(f)

            for log_map in logs_map:
                gps_data = GeoLocalizationData(
                    x=log_map['x'],
                    y=log_map['y'],
                    z=log_map['z'],
                    time_s=log_map['t'],
                    barometric_height=log_map['z'],
                    gps_height=log_map['z'],
                    pitch=None,
                    roll=None,
                    yaw=None,
                    image_identifier=log_map['image']
                )
                gps_data_list.append(gps_data)

        return gps_data_list

    def get_log_by_image_name(self, image_name: str) -> GeoLocalizationData:

        image_identifier = image_name.split(".")[0]

        logs = self.get_logs()

        for log in logs:

            if log.image_identifier == image_identifier:
                return log

        raise Exception("no log for given image_name found")
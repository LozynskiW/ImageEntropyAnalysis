import numpy as np

from target_detection_validation_interfaces import base


class SizeBased(base):

    def validate(self, target_coordinates, camera):

        try:
            img_horizontal_dim_in_meters = 2 * np.tan((np.pi / 180) * 0.5 * self.__object_geo_loc_calculator.get_camera_horizontal_fov()) * self.__distance_to_object
            img_vertical_dim_in_meters = 2 * np.tan((np.pi / 180) * 0.5 * self.__object_geo_loc_calculator.get_camera_vertical_fov()) * self.__distance_to_object
        except TypeError:
            return False

        acceptable_fill_factor = max_object_dim ** 2 / (img_horizontal_dim_in_meters * img_vertical_dim_in_meters)

        return acceptable_fill_factor < self.__fill_factor

    @staticmethod
    def __calculate_distance_to_object(log):
        if log is not None:
            print("Distance:", np.abs(float(log['barometric_height']) / (np.cos(float(log['pitch']) * np.pi / 180))))
            return np.abs(float(log['barometric_height']) / (np.cos(float(log['pitch']) * np.pi / 180)))
        return None

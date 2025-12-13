from enum import StrEnum


class MapKeysEnum:

    @classmethod
    def values(cls):
        return {e for e in cls}


class PersistentNames(MapKeysEnum, StrEnum):
    """
    Enum to store keys of values that are saved into db
    """
    OBJECT = "object"
    DATASET = "dataset"
    FILE_NAME = "file_name"

    HISTOGRAM_OF_ORIGINAL_IMAGE = "histogram_of_original_image"
    HISTOGRAM_NORMALIZED_OF_ORIGINAL_IMAGE = "histogram_normalized_of_original_image"
    EXPECTED_VALUE_OF_ORIGINAL_IMAGE = "expected_value_of_original_image"
    VARIANCE_OF_ORIGINAL_IMAGE = "variance_of_original_image"
    STANDARD_DEVIATION_OF_ORIGINAL_IMAGE = "standard_deviation_of_original_image"
    INFORMATION_FOR_X_OF_ORIGINAL_IMAGE = "information_for_x_of_original_image"
    INFORMATION_IN_BITS_OF_ORIGINAL_IMAGE = "information_in_bits_of_original_image"
    ENTROPY_FOR_X_OF_ORIGINAL_IMAGE = "entropy_for_x_of_original_image"
    ENTROPY_IN_BITS_OF_ORIGINAL_IMAGE = "entropy_in_bits_of_original_image"

    HISTOGRAM_OF_PROCESSED_IMAGE = "histogram_of_processed_image"
    HISTOGRAM_NORMALIZED_OF_PROCESSED_IMAGE = "histogram_normalized_of_processed_image"
    EXPECTED_VALUE_OF_PROCESSED_IMAGE = "expected_value_of_processed_image"
    VARIANCE_OF_PROCESSED_IMAGE = "variance_of_processed_image"
    STANDARD_DEVIATION_OF_PROCESSED_IMAGE = "standard_deviation_of_processed_image"
    INFORMATION_FOR_X_OF_PROCESSED_IMAGE = "information_for_x_of_processed_image"
    INFORMATION_IN_BITS_OF_PROCESSED_IMAGE = "information_in_bits_of_processed_image"
    ENTROPY_FOR_X_OF_PROCESSED_IMAGE = "entropy_for_x_of_processed_image"
    ENTROPY_IN_BITS_OF_PROCESSED_IMAGE = "entropy_in_bits_of_processed_image"

    X = "x"
    Y = "y"
    Z = "z"
    TIME_S = "time_s"
    BAROMETRIC_HEIGHT = "barometric_height"
    GPS_HEIGHT = "gps_height"
    PITCH = "pitch"
    ROLL = "roll"
    YAW = "yaw"


class TransientValues(MapKeysEnum, StrEnum):
    """
    Enum to store keys of values that are not saved into db
    """
    HISTOGRAM_VALUES = "histogram_values"


class KeyValues(MapKeysEnum, StrEnum):
    """
    Enum to store keys of values that can be used to index DataMaps
    """
    DISTANCE = "distance"
    BAROMETRIC_HEIGHT = "barometric_height"
    GPS_HEIGHT = "gps_height"
    PITCH = "pitch"

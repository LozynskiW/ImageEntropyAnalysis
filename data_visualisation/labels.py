from copy import copy

from data_unification.enums import PersistentNames, TransientValues, KeyValues, MapKeysEnum


class Label:

    @staticmethod
    def _get_labels_dict():
        return {
            # PersistentNames.OBJECT: "object"
            # PersistentNames.DATASET: "dataset"
            # PersistentNames.FILE_NAME: "file_name"

            # PersistentNames.HISTOGRAM_OF_ORIGINAL_IMAGE: "histogram_of_original_image"
            # PersistentNames.HISTOGRAM_NORMALIZED_OF_ORIGINAL_IMAGE: "histogram_normalized_of_original_image"
            PersistentNames.EXPECTED_VALUE_OF_ORIGINAL_IMAGE: "Eo(X) [luminance]",
            PersistentNames.VARIANCE_OF_ORIGINAL_IMAGE: "S2o (X)",
            PersistentNames.STANDARD_DEVIATION_OF_ORIGINAL_IMAGE: "σo(X) [luminance]",
            PersistentNames.INFORMATION_FOR_X_OF_ORIGINAL_IMAGE: "Io(x) [bit]",
            PersistentNames.INFORMATION_IN_BITS_OF_ORIGINAL_IMAGE: "Io(X) [bit]",
            PersistentNames.ENTROPY_FOR_X_OF_ORIGINAL_IMAGE: "Ho(x)=%s [bit]",
            PersistentNames.ENTROPY_IN_BITS_OF_ORIGINAL_IMAGE: "Ho(X) [bit]",

            # PersistentNames.HISTOGRAM_OF_PROCESSED_IMAGE: "histogram_of_processed_image"
            # PersistentNames.HISTOGRAM_NORMALIZED_OF_PROCESSED_IMAGE: "histogram_normalized_of_processed_image"
            PersistentNames.EXPECTED_VALUE_OF_PROCESSED_IMAGE: "E(X) [luminance]",
            PersistentNames.VARIANCE_OF_PROCESSED_IMAGE: "S2 (X)",
            PersistentNames.STANDARD_DEVIATION_OF_PROCESSED_IMAGE: "σ(X) [luminance]",
            PersistentNames.INFORMATION_FOR_X_OF_PROCESSED_IMAGE: "I(x) [bit]",
            PersistentNames.INFORMATION_IN_BITS_OF_PROCESSED_IMAGE: "I(X) [bit]",
            PersistentNames.ENTROPY_FOR_X_OF_PROCESSED_IMAGE: "H(x)=%s [bit]",
            PersistentNames.ENTROPY_IN_BITS_OF_PROCESSED_IMAGE: "H(X) [bit]",

            PersistentNames.X: "x[m]",
            PersistentNames.Y: "y[m]",
            PersistentNames.Z: "z[m]",
            PersistentNames.TIME_S: "t[s]",
            # PersistentNames.BAROMETRIC_HEIGHT: "barometric_height"
            # PersistentNames.GPS_HEIGHT: "gps_height"
            PersistentNames.PITCH: "β[°]",
            # PersistentNames.ROLL: "roll"
            # PersistentNames.YAW: "yaw"

            # TransientValues.HISTOGRAM_VALUES: "histogram_values"
            TransientValues.NUMBER_OF_PIXELS: "N",

            KeyValues.DISTANCE: "d[m]"
            # KeyValues.BAROMETRIC_HEIGHT_KV: "barometric_height"
            # KeyValues.GPS_HEIGHT_KV: "gps_height"
            # KeyValues.PITCH_KV: "pitch"
        }

    @classmethod
    def get_symbol(cls, key: MapKeysEnum | str):

        key_enum = copy(key)

        if key_enum in cls._get_labels_dict():
            return cls._get_labels_dict().get(key_enum)
        else:
            return key_enum

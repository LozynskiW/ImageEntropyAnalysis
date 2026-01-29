import copy
import math
from abc import ABC

import numpy as np
from numpy import mean

from data_unification.data_map.models import DataMap, DataRow
from data_unification.enums import PersistentNames, TransientValues, KeyValues, MapKeysEnum
from image_processing.basictools.statisticalparameters import normalize_histogram, exp_val_from_histogram, \
    variance_from_histogram, std_dev_from_variance, information_for_histogram, \
    information_entropy_values_from_histogram, information_entropy_for_histogram


class _DataRow(DataRow):
    """
    Structure to keep given data immutable, where data row is one document from whole group of documents
    """
    _data_row: dict

    def __init__(self, data: dict):

        if len(data.keys()) == 0:
            raise ValueError("No keys in data, data should be dict")

        if data.keys() != PersistentNames.values():
            raise ValueError("Data must contain the same keys as are in ValuesNames")

        self._data_row = copy.deepcopy(data)
        self._calculate_values()

    def get_value(self, key: MapKeysEnum):
        return copy.deepcopy(self._data_row.get(key.value))

    def _calculate_values(self):

        self._data_row[TransientValues.HISTOGRAM_VALUES.value] = range(len(self._data_row.get(
            PersistentNames.HISTOGRAM_OF_ORIGINAL_IMAGE.value)))

        self._data_row[TransientValues.NUMBER_OF_PIXELS] = sum(self._data_row[PersistentNames.HISTOGRAM_OF_PROCESSED_IMAGE])
        self._data_row[TransientValues.LOG10_NUMBER_OF_PIXELS] = np.log10(self._data_row[TransientValues.NUMBER_OF_PIXELS])

        self._data_row[KeyValues.DISTANCE.value] = float(math.sqrt(
            math.pow(self._data_row[PersistentNames.X.value], 2) +
            math.pow(self._data_row[PersistentNames.Y.value], 2) +
            math.pow(self._data_row[PersistentNames.Z.value], 2)
        ))

        pitch_tan = self._data_row[PersistentNames.X.value] / self._data_row[PersistentNames.Z.value]
        self._data_row[KeyValues.PITCH.value] = float(math.atan(pitch_tan) * 180 / math.pi)

    def _set_value(self, key: PersistentNames | TransientValues, value):
        self._data_row[key.value] = value


class ImageEntropyAnalysisDataMap(DataMap):
    _data_rows: list[_DataRow]

    def __init__(self, data_from_db: list[dict], indexes: set[KeyValues], histogram_values_to_ignore: list = []):
        """
        Parameters
        ----------
        data_from_db
        indexes: values that will be used to index data based on values
        histogram_values_to_ignore: list of histogram values (also positions on array so 0 means histogram[0]) to remove
        from calculations of statistical parameters
        """

        self._data_rows = []

        if len(data_from_db) == 0:
            raise ValueError("No data, provided data should be non empty list[dict]")

        if len(data_from_db[0].keys()) == 0:
            raise ValueError("No keys in data, should be dict")

        for data_row in data_from_db:
            self._data_rows.append(_DataRow(data_row))

        if len(histogram_values_to_ignore) > 0:
            self._recalculate_without_values(histogram_values_to_ignore)

        self._index_data_maps(indexes)

    def get_values(self, key: MapKeysEnum) -> list:
        if key in self._data_map_indexes.keys():
            return self._get_values_from_index(key)
        else:
            return self._get_values_from_data_rows(key)

    def get_values_by(self, key: MapKeysEnum, min_val: float, max_val: float) -> list:
        return list(filter(lambda v: min_val <= v < max_val, self.get_values(key)))

    def get_values_for_where(self, values_key: MapKeysEnum,
                             values_where_key: MapKeysEnum,
                             min_val: float,
                             max_val: float) -> list:

        data_rows_for_values_where = list(filter(lambda dr:  min_val <= dr.get_value(values_where_key) <= max_val, self._data_rows))

        return list(map(lambda dr: dr.get_value(values_key), data_rows_for_values_where))

    def get_indexes(self) -> dict[KeyValues, list[float]]:
        indexes = {}
        for k in self._data_map_indexes.keys():
            indexes[k] = list(self._data_map_indexes.get(k).keys())

        return indexes

    def _get_values_from_index(self, key: MapKeysEnum) -> list:
        index_for_key: dict[float, list[_DataRow]] = self._data_map_indexes.get(key)
        values = []

        for idx_val in index_for_key:
            data_rows = index_for_key.get(idx_val)
            values.extend(list(map(lambda dr: dr.get_value(key), data_rows)))

        return values

    def _get_values_from_data_rows(self, key: MapKeysEnum) -> list:
        return list(map(lambda dr: dr.get_value(key), self._data_rows))

    def _index_data_maps(self, indexes: set[KeyValues]):

        self._data_map_indexes = {}

        for idx in indexes:
            self._data_map_indexes[idx] = {}
            new_keys_map: dict[float, list[_DataRow]] = {}

            for dr in self._data_rows:

                indexed_value = dr.get_value(idx)

                if indexed_value in new_keys_map:
                    new_keys_map.get(indexed_value).append(dr)
                else:
                    new_keys_map[indexed_value] = [dr]

            self._data_map_indexes[idx] = new_keys_map

    def _get_values_by_key_and_value(self, key_index: KeyValues, value) -> list:
        if key_index not in self._data_map_indexes.keys():
            raise KeyError("no such key index, You must add one to be able to use this method")
        data_rows_for_key = self._data_map_indexes[key_index].get(value)

        return list(map(lambda dr: dr.get_value(key_index), data_rows_for_key))

    def _recalculate_without_values(self, histogram_values_to_remove: list):

        for dr in self._data_rows:
            grayscale = list(dr.get_value(TransientValues.HISTOGRAM_VALUES))

            for v in histogram_values_to_remove:
                if v in grayscale:
                    grayscale.remove(v)

            histogram_processed_img: list = dr.get_value(PersistentNames.HISTOGRAM_OF_PROCESSED_IMAGE)

            offset = 0
            for i in histogram_values_to_remove:
                histogram_processed_img.pop(i-offset)
                offset += 1

            number_of_pixels = sum(histogram_processed_img)
            log10_num_of_pixels = np.log10(number_of_pixels)
            histogram_normalized = normalize_histogram(histogram_processed_img)
            exp_val = exp_val_from_histogram(grayscale=grayscale, gray_shade_prob=histogram_normalized)
            variance = variance_from_histogram(grayscale=grayscale,
                                               gray_shade_prob=histogram_normalized,
                                               expected_value=exp_val)
            std_dev = std_dev_from_variance(variance)
            information_for_values = information_for_histogram(histogram_probabilities=histogram_normalized)
            information = float(sum(information_for_values))
            information_entropy_for_values = information_entropy_values_from_histogram(
                histogram_values=grayscale,
                histogram_probabilities=histogram_normalized
            )
            information_entropy = information_entropy_for_histogram(histogram_values=grayscale,
                                                                    histogram_probabilities=histogram_normalized)

            dr._set_value(TransientValues.HISTOGRAM_VALUES, grayscale)

            dr._set_value(TransientValues.NUMBER_OF_PIXELS, number_of_pixels)

            dr._set_value(TransientValues.LOG10_NUMBER_OF_PIXELS, log10_num_of_pixels)

            dr._set_value(PersistentNames.HISTOGRAM_OF_PROCESSED_IMAGE, histogram_processed_img)

            dr._set_value(PersistentNames.HISTOGRAM_NORMALIZED_OF_PROCESSED_IMAGE, histogram_normalized)

            dr._set_value(PersistentNames.EXPECTED_VALUE_OF_PROCESSED_IMAGE, exp_val)

            dr._set_value(PersistentNames.VARIANCE_OF_PROCESSED_IMAGE, variance)

            dr._set_value(PersistentNames.STANDARD_DEVIATION_OF_PROCESSED_IMAGE, std_dev)

            dr._set_value(PersistentNames.INFORMATION_FOR_X_OF_PROCESSED_IMAGE, information_for_values)

            dr._set_value(PersistentNames.INFORMATION_IN_BITS_OF_PROCESSED_IMAGE, information)

            dr._set_value(PersistentNames.ENTROPY_FOR_X_OF_PROCESSED_IMAGE, information_entropy_for_values)

            dr._set_value(PersistentNames.ENTROPY_IN_BITS_OF_PROCESSED_IMAGE, information_entropy)


class SortableDataMap(DataMap, ABC):
    _data_map: ImageEntropyAnalysisDataMap
    _indexes: dict[KeyValues, list[float]]

    def __init__(self, data_map: ImageEntropyAnalysisDataMap, sorting_function=sorted):
        self._data_map = data_map
        self._sort(sorting_function)

    def _sort(self, sorting_function):

        self._indexes = {}
        data_map_indexes_to_sort = self._data_map.get_indexes()

        for idx_key in data_map_indexes_to_sort:
            values_to_sort = data_map_indexes_to_sort.get(idx_key)

            sorted_values = list(sorting_function(values_to_sort))

            self._indexes[idx_key] = sorted_values

    def get_values(self, key: MapKeysEnum) -> list:

        if key in self._indexes.keys():
            out_list = []

            for v in self._indexes.get(key):
                out_list.extend(self._data_map._get_values_by_key_and_value(key_index=key, value=v))

            return out_list
        else:
            return self._data_map.get_values(key)

    def get_values_by(self, key: MapKeysEnum, min_val: float, max_val: float) -> list:
        return self._data_map.get_values_by(key, min_val, max_val)

    def get_values_for_where(self, values_key: MapKeysEnum, values_where_key: MapKeysEnum, min_val: float, max_val: float) -> list:
        return self._data_map.get_values_for_where(values_key, values_where_key, min_val, max_val)

    def get_data_map_indexes(self) -> dict[KeyValues, dict[float, list[DataRow]]]:
        return self._data_map.get_data_map_indexes()

    def _get_values_by_key_and_value(self, key_index: KeyValues, value) -> list:
        return self._data_map._get_values_by_key_and_value(key_index, value)


class TakingNthValueDataMap(DataMap, ABC):
    _data_map: DataMap
    _indexes: dict[KeyValues, list[float]]
    _take_nth: int

    def __init__(self, data_map: DataMap, take_nth=5):
        self._data_map = data_map
        self._take_nth = take_nth

    def get_values(self, key: MapKeysEnum) -> list:
        values = self._data_map.get_values(key)
        i = 0
        nth_values = []

        for v in values:
            if i % self._take_nth == 0:
                nth_values.append(v)
            i += 1
        return nth_values

    def get_values_by(self, key: MapKeysEnum, min_val: float, max_val: float) -> list:
        return self._data_map.get_values_by(key, min_val, max_val)

    def get_values_for_where(self, values_key: MapKeysEnum, values_where_key: MapKeysEnum, min_val: float, max_val: float) -> list:
        return self._data_map.get_values_for_where(values_key, values_where_key, min_val, max_val)

    def get_data_map_indexes(self) -> dict[KeyValues, dict[float, list[DataRow]]]:
        return self._data_map.get_data_map_indexes()

    def _get_values_by_key_and_value(self, key_index: KeyValues, value) -> list:
        return self._data_map._get_values_by_key_and_value(key_index, value)


class DistinctHorizontallyDataMap(DataMap, ABC):
    _data_map: DataMap

    def __init__(self, data_map: DataMap):
        self._data_map = data_map

    def get_values(self, key: MapKeysEnum) -> list:
        indexes = self._data_map.get_data_map_indexes()
        distinct_values = []

        if key in KeyValues:
            indexed_vals = indexes.get(key)

            for dr_list in indexed_vals.values():
                val_for_key = mean(list(map(lambda dr: dr.get_value(key), dr_list)))
                distinct_values.append(val_for_key)
        else:
            indexes_keys = indexes.keys()
            indexed_vals = indexes.get(list(indexes_keys)[0])

            for dr_list in indexed_vals.values():
                val_for_key = mean(list(map(lambda dr: dr.get_value(key), dr_list)))
                distinct_values.append(val_for_key)

        return distinct_values

    def get_values_by(self, key: MapKeysEnum, min_val: float, max_val: float) -> list:
        return self._data_map.get_values_by(key, min_val, max_val)

    def get_values_for_where(self, values_key: MapKeysEnum, values_where_key: MapKeysEnum, min_val: float, max_val: float) -> list:
        return self._data_map.get_values_for_where(values_key, values_where_key, min_val, max_val)

    def get_data_map_indexes(self) -> dict[KeyValues, dict[float, list[DataRow]]]:
        return self._data_map.get_data_map_indexes()

    def _get_values_by_key_and_value(self, key_index: KeyValues, value) -> list:
        return self._data_map._get_values_by_key_and_value(key_index, value)


class DistinctVerticallyDataMap(DataMap, ABC):
    """
    Can only be used after DistinctHorizontallyDataMap
    """
    _data_map: DataMap
    _key_to_uniform: KeyValues = None

    def __init__(self, data_map: DataMap, key_to_uniform: KeyValues):
        self._data_map = data_map
        self._key_to_uniform = key_to_uniform

        # smallest_len = 100000000
        # all_indexes = self.get_data_map_indexes()
        #
        # for idx_key in all_indexes:
        #     index_len = len(all_indexes.get(idx_key).keys())
        #     if index_len < smallest_len:
        #         smallest_len = index_len
        #         self._shortest_distinct_index = idx_key
        #
        # if self._shortest_distinct_index is None:
        #     raise ValueError("No value for _shortest_distinct_index - check if there are any indexes in given DataMap")

    def get_values(self, key: MapKeysEnum) -> list:
        dist_values_for_key = list(set(self._data_map.get_values(self._key_to_uniform)))

        values = self._data_map.get_values(key)

        if len(values) == len(dist_values_for_key):
            return values

        else:
            vals = []
            index_for_value = self.get_data_map_indexes().get(self._key_to_uniform)

            unique_vals = list(set(index_for_value.keys()))

            for f_val in unique_vals:
                data_rows = index_for_value.get(f_val)
                vals.append(data_rows[0].get_value(key))

            return vals

    def get_values_by(self, key: MapKeysEnum, min_val: float, max_val: float) -> list:
        return self._data_map.get_values_by(key, min_val, max_val)

    def get_values_for_where(self, values_key: MapKeysEnum, values_where_key: MapKeysEnum, min_val: float, max_val: float) -> list:
        return self._data_map.get_values_for_where(values_key, values_where_key, min_val, max_val)

    def get_data_map_indexes(self) -> dict[KeyValues, dict[float, list[DataRow]]]:
        return self._data_map.get_data_map_indexes()

    def _get_values_by_key_and_value(self, key_index: KeyValues, value) -> list:
        return self._data_map._get_values_by_key_and_value(key_index, value)


class SmoothingDataMap(DataMap, ABC):
    _data_map: DataMap
    _smoothing_window: int

    def __init__(self, data_map: DataMap, smoothing_window=5):
        self._data_map = data_map
        self._smoothing_window = smoothing_window

    def get_values(self, key: MapKeysEnum) -> list:
        values = self._data_map.get_values(key)

        smoothed_values = []

        window_len = int(self._smoothing_window / 2)
        max_smoothing_idx = len(values) - window_len

        for i in range(0, window_len):
            smoothed_values.append(values[i])

        for i in range(window_len, max_smoothing_idx):
            avr = mean(values[i - window_len:i + window_len])
            smoothed_values.append(avr)

        for i in range(max_smoothing_idx - window_len, max_smoothing_idx):
            smoothed_values.append(values[i])

        return smoothed_values

    def get_values_by(self, key: MapKeysEnum, min_val: float, max_val: float) -> list:
        return self._data_map.get_values_by(key, min_val, max_val)

    def get_values_for_where(self, values_key: MapKeysEnum, values_where_key: MapKeysEnum, min_val: float, max_val: float) -> list:
        return self._data_map.get_values_for_where(values_key, values_where_key, min_val, max_val)

    def get_data_map_indexes(self) -> dict[KeyValues, dict[float, list[DataRow]]]:
        return self._data_map.get_data_map_indexes()

    def _get_values_by_key_and_value(self, key_index: KeyValues, value) -> list:
        return self._data_map._get_values_by_key_and_value(key_index, value)

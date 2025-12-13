import math

import numpy as np


class ReducingFunctions:

    @staticmethod
    def mean(data_from_db, data_to_reduce_to):
        return np.mean(map(lambda x: x[data_to_reduce_to], data_from_db))

    @staticmethod
    def lowest_value(data_from_db, data_to_reduce_to):
        return np.min(map(lambda x: x[data_to_reduce_to], data_from_db))

    @staticmethod
    def highest_value(data_from_db, data_to_reduce_to):
        return np.max(map(lambda x: x[data_to_reduce_to], data_from_db))

    @staticmethod
    def absolute_val(x, y):
        return math.sqrt(math.pow(x, 2) + math.pow(y, 2))

    @staticmethod
    def absolute_val_double_tuples(tuple_list: list[tuple]):
        return list(map(lambda v: math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2)), tuple_list))

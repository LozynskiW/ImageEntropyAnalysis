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

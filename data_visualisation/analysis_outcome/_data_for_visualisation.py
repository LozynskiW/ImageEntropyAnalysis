import numpy as np


class Single3DPoint:
    __x = 0.0
    __y = 0.0
    __z = 0.0

    def __init__(self, x=0, y=0, z=0):
        self.__x = x
        self.__y = y
        self.__z = z

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z

    def __str__(self):
        return "[ x = " + str(self.__x) + ", y = " + str(self.__y) + ", z = " + str(self.__z)


class SingleDataset:
    __x_axis = []
    __y_axis = []

    def __init__(self, x_axis=None, y_axis=None):
        if y_axis is None:
            y_axis = []
        if x_axis is None:
            x_axis = []
        self.__x_axis = x_axis
        self.__y_axis = y_axis

    @property
    def x_axis(self):
        return self.__x_axis

    @property
    def y_axis(self):
        return self.__y_axis


class SingleDataset3D(SingleDataset):
    __z_axis = []

    def __init__(self, x_axis=None, y_axis=None, z_axis=None):
        super().__init__(x_axis, y_axis)
        self.__z_axis = z_axis

    @property
    def z_axis(self):
        return self.__z_axis


class MultipleDatasets:
    __datasets = []

    def __init__(self, datasets):
        for dataset in datasets:
            if not isinstance(dataset, SingleDataset):
                raise TypeError("All elements in datasets must be of type SingleDataset")
        self.__datasets = datasets

    @property
    def datasets(self):
        return self.__datasets


class MultipleDatasetsValuesMap:
    # __facade_datasets_map = None
    __heatmap = None
    __points_3d_array = []
    __x_labels = []
    __y_labels = []

    def __init__(self, points_3d_array: [Single3DPoint], x_labels, y_labels):
        self.__datasets_map = np.zeros((len(y_labels), len(x_labels)))
        self.__points_3d_array = points_3d_array
        self.__x_labels = x_labels
        self.__y_labels = y_labels
        # self._build_facade()

    @property
    def datasets_map(self):
        return self.__datasets_map

    @property
    def x_labels(self):
        return self.__x_labels

    @property
    def y_labels(self):
        return self.__y_labels

    @property
    def points_3d_array(self):
        return self.__points_3d_array

    def get_point_for_x_y(self, x_label, y_label):
        for p in self.__points_3d_array:
            if p.x == x_label and p.y == y_label:
                return p.z
        return 0

    @staticmethod
    def are_all_items_in_arr_numeric(array):
        return all(list(map(lambda x: isinstance(x, (int, float, complex)) and not isinstance(x, bool) ,array)))

    # def _set_labels_for_facade(self):
    #     if MultipleDatasetsValuesMap.are_all_items_in_arr_numeric(self.__x_labels):
    #         min_value = min(self.__x_labels)
    #         max_value = max(self.__x_labels)
    #
    #         if (np.abs(self.__x_labels[1] - self.__x_labels[0]) == np.abs(self.__x_labels[2] - self.__x_labels[1])):
    #             step = np.abs(self.__x_labels[1] - self.__x_labels[0])
    #         else:
    #             step =
    #
    #         new_x_labels = [min_value]
    #         while max(new_x_labels) <= max_value:
    #             new_x_labels.append(new_x_labels[-1] + step)
    #
    #         self.__x_labels = new_x_labels

    # def _build_facade(self):
    #     for x in np.arange(len(self.__x_labels)):
    #         for y in np.arange(len(self.__y_labels)):
    #             self.__facade_datasets_map[y][x] = Single3DPoint()

class MultipleDatasets3D:
    __datasets = []

    def __init__(self, datasets):
        for dataset in datasets:
            if not isinstance(dataset, SingleDataset3D):
                raise TypeError("All elements in datasets must be of type SingleDataset")
        self.__datasets = datasets

    @property
    def datasets(self):
        return self.__datasets

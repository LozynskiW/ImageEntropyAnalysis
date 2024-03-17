
class SingleDataset:
    __x_axis = []
    __y_axis = []

    def __init__(self, x_axis, y_axis):
        self.__x_axis = x_axis
        self.__y_axis = y_axis

    @property
    def x_axis(self):
        return self.__x_axis

    @property
    def y_axis(self):
        return self.__y_axis


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
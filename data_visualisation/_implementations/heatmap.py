import numpy as np
from matplotlib import pyplot as plt

from data_visualisation.analysis_outcome._data_for_visualisation import MultipleDatasetsValuesMap, Single3DPoint
from data_visualisation.models import PlotOptions, FigureOptions


class Heatmap:

    def __init__(self):
        self.__datasets_map = None

    @staticmethod
    def plot_data(data_from_db, figure_options: FigureOptions = FigureOptions()):

        datasets_map = Heatmap.__build_single_dataset_value_map(
            data_from_db=data_from_db,
            data_to_x_axis=figure_options.x_axis_label,
            data_to_y_axis=figure_options.y_axis_label,
            data_as_map_value=figure_options.z_axis_label
        )

        figure, ax = plt.subplots()
        heatmap = datasets_map.datasets_map

        for y in np.arange(len(datasets_map.y_labels)):
            for x in np.arange(len(datasets_map.x_labels)):
                heatmap[y][x] = datasets_map.get_point_for_x_y(datasets_map.x_labels[x],
                                                               datasets_map.y_labels[y])

        im = ax.imshow(heatmap)
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel(figure_options.z_axis_label, rotation=-90, va="bottom")
        ax.set_xticks(np.arange(len(datasets_map.x_labels)), labels=datasets_map.x_labels)
        ax.set_yticks(np.arange(len(datasets_map.y_labels)), labels=datasets_map.y_labels)
        ax.set_xlabel(figure_options.x_axis_label)
        ax.set_ylabel(figure_options.y_axis_label)
        plt.show()

    @staticmethod
    def __build_single_dataset_value_map(data_from_db: list,
                                         data_to_x_axis,
                                         data_to_y_axis,
                                         data_as_map_value,
                                         mapping_fun=None) -> MultipleDatasetsValuesMap:
        data_as_points = []

        for d in data_from_db:

            if mapping_fun is None:
                point = Single3DPoint(x=float(d[data_to_x_axis]),
                                      y=float(d[data_to_y_axis]),
                                      z=float(d[data_as_map_value]))
            else:
                point = Single3DPoint(x=float(d[data_to_x_axis]),
                                      y=float(d[data_to_y_axis]),
                                      z=float(mapping_fun(d[data_as_map_value])))

            data_as_points.append(point)

        x_labels = list(map(lambda x: x[data_to_x_axis], data_from_db))
        y_labels = list(map(lambda x: x[data_to_y_axis], data_from_db))

        x_labels_sorted_distinct = np.sort(list(set(x_labels)))
        y_labels_sorted_distinct = np.sort(list(set(y_labels)))

        return MultipleDatasetsValuesMap(points_3d_array=data_as_points,
                                         x_labels=x_labels_sorted_distinct,
                                         y_labels=list(reversed(y_labels_sorted_distinct))
                                         # needed so y axis values are sorted from lowest(bottom) to highest(top)
                                         )

from dataclasses import dataclass

import numpy as np
from matplotlib import pyplot as plt

from data_visualisation.analysis_outcome._data_for_visualisation import MultipleDatasetsValuesMap, Single3DPoint
from data_visualisation.models import FigureOptions

from typing import Callable


@dataclass
class HeatmapConfig:
    show_cbar: bool = True
    show_annotations: bool = True
    to_percentage: bool = False
    values_mapping_fun: Callable = None,
    dpi: int = 200


class Heatmap:

    def __init__(self):
        self.__datasets_map = None

    @staticmethod
    def plot_data(data_from_db,
                  figure_options: FigureOptions = FigureOptions(),
                  config: HeatmapConfig = HeatmapConfig()):

        Heatmap.__create_heatmap(data_from_db, figure_options, config)

        plt.show()

    @staticmethod
    def save_to_file(data_from_db,
                     figure_options: FigureOptions = FigureOptions(),
                     config: HeatmapConfig = HeatmapConfig(),
                     file_name: str = "heatmap"):

        Heatmap.__create_heatmap(data_from_db, figure_options, config)

        plt.savefig(fname=file_name, dpi=config.dpi)

    @staticmethod
    def __create_heatmap(data_from_db, figure_options: FigureOptions, config: HeatmapConfig):
        datasets_map = Heatmap.__build_value_map(
            data_from_db=data_from_db,
            data_to_x_axis=figure_options.x_axis_label,
            data_to_y_axis=figure_options.y_axis_label,
            data_as_map_value=figure_options.z_axis_label,
            mapping_fun=config.values_mapping_fun
        )

        figure, ax = plt.subplots()
        heatmap = datasets_map.datasets_map

        for y in np.arange(len(datasets_map.y_labels)):
            for x in np.arange(len(datasets_map.x_labels)):
                heatmap[y][x] = datasets_map.get_point_for_x_y(datasets_map.x_labels[x],
                                                               datasets_map.y_labels[y])
        if config.show_annotations:
            Heatmap.__set_annotations_to_heatmap(ax, heatmap, to_percentage=config.to_percentage)

        im = ax.imshow(heatmap)
        if config.show_cbar:
            cbar = ax.figure.colorbar(im, ax=ax)
            cbar.ax.set_ylabel(figure_options.z_axis_label, rotation=-90, va="bottom")

        Heatmap.__set_figure_labels_title(ax=ax, datasets_map=datasets_map, figure_options=figure_options)

    @staticmethod
    def __set_figure_labels_title(ax, datasets_map: MultipleDatasetsValuesMap, figure_options: FigureOptions):
        ax.set_xticks(np.arange(len(datasets_map.x_labels)), labels=datasets_map.x_labels)
        ax.set_yticks(np.arange(len(datasets_map.y_labels)), labels=datasets_map.y_labels)

        ax.set_xlabel(figure_options.x_axis_label)
        ax.set_ylabel(figure_options.y_axis_label)
        ax.set_title(figure_options.title)

    @staticmethod
    def __set_annotations_to_heatmap(ax, heatmap_values, to_percentage=False):
        divisor = 1
        if to_percentage:
            divisor = max(map(max, heatmap_values))

        for y in np.arange(len(heatmap_values)):
            for x in np.arange(len(heatmap_values[0])):
                ax.text(x, y, round(heatmap_values[y, x] / divisor, 2), ha="center", va="center", color="w")

    @staticmethod
    def __build_value_map(data_from_db: list,
                          data_to_x_axis,
                          data_to_y_axis,
                          data_as_map_value,
                          mapping_fun=None) -> MultipleDatasetsValuesMap:
        data_as_points = []

        if mapping_fun is None:
            mapping_fun = lambda x: x[data_as_map_value]

        for d in data_from_db:
            point = Single3DPoint(x=float(d[data_to_x_axis]),
                                  y=float(d[data_to_y_axis]),
                                  z=float(mapping_fun(d)))
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

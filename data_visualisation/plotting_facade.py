import numpy as np
from matplotlib import pyplot as plt

from data_unification._utils import build_multiple_datasets, build_multiple_datasets_3d, \
    build_multiple_datasets_value_map
from data_visualisation.consts.plot_options import PlotOptions
from data_visualisation.util.figure_and_plot_style import FigureBuilder
from matplotlib import cm


class Plots2D:
    figure_builder = FigureBuilder()

    def __init__(self, data_from_db, plot_options: PlotOptions):
        self.__plot_options = plot_options
        self.__datasets = build_multiple_datasets(
            data_from_db=data_from_db,
            data_to_x_axis=plot_options.x_axis,
            data_to_y_axis=plot_options.y_axis
        )

    def scatter_plot(self):

        figure = self.figure_builder.build()

        for dataset in self.__datasets.datasets:
            figure.scatter(x=dataset.x_axis,
                           y=dataset.y_axis)
        plt.show()

    def line_plot(self):
        figure = self.figure_builder.build()

        for dataset in self.__datasets.datasets:
            figure.line(x=dataset.x_axis,
                        y=dataset.y_axis)
        plt.show()

    def bar_plot(self):
        figure = self.figure_builder.build()

        for dataset in self.__datasets.datasets:
            figure.bar(x=dataset.x_axis,
                       y=dataset.y_axis)
        plt.show()


class Heatmap:

    def __init__(self, data_from_db, plot_options: PlotOptions):
        self.__plot_options = plot_options
        self.__datasets_map = build_multiple_datasets_value_map(
            data_from_db=data_from_db,
            data_to_x_axis=plot_options.x_axis,
            data_to_y_axis=plot_options.y_axis,
            data_as_map_value=plot_options.z_axis
        )

    def reduce_to_means(self):
        figure, ax = plt.subplots()
        heatmap = self.__datasets_map.datasets_map

        for y in np.arange(len(self.__datasets_map.y_labels)):
            for x in np.arange(len(self.__datasets_map.x_labels)):
                heatmap[y][x] = self.__datasets_map.get_point_for_x_y(self.__datasets_map.x_labels[x],self.__datasets_map.y_labels[y])

        im = ax.imshow(heatmap)
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel(self.__plot_options.z_axis, rotation=-90, va="bottom")
        ax.set_xticks(np.arange(len(self.__datasets_map.x_labels)), labels=self.__datasets_map.x_labels)
        ax.set_yticks(np.arange(len(self.__datasets_map.y_labels)), labels=self.__datasets_map.y_labels)
        ax.set_xlabel(self.__plot_options.x_axis)
        ax.set_ylabel(self.__plot_options.y_axis)
        plt.show()


class Plots3D:
    figure_builder = FigureBuilder()

    def __init__(self, data_from_db, plot_options: PlotOptions):
        self.__plot_options = plot_options
        self.__datasets = build_multiple_datasets_3d(
            data_from_db=data_from_db,
            data_to_x_axis=plot_options.x_axis,
            data_to_y_axis=plot_options.y_axis,
            data_to_z_axis=plot_options.z_axis
        )

    def bar_plot(self):
        figure = plt.figure()

        for dataset in self.__datasets.datasets:
            ax = figure.add_subplot(projection='3d')

            minValueOfXAxis = min(dataset.x_axis)
            maxValueOfXAxis = max(dataset.x_axis)

            xedges = np.linspace(minValueOfXAxis, maxValueOfXAxis)

            minValueOfYAxis = min(dataset.y_axis)
            maxValueOfYAxis = max(dataset.y_axis)

            yedges = np.linspace(minValueOfYAxis, maxValueOfYAxis)

            xpos, ypos = np.meshgrid(xedges[:-1] + minValueOfXAxis, yedges[:-1] + minValueOfYAxis, indexing="ij")
            zpos = 0

            # Construct arrays with the dimensions for the 16 bars.

            ax.bar3d(xpos, ypos, zpos, dataset.x_axis, dataset.y_axis, dataset.z_axis, zsort='average')

            plt.show()
            figure.bar(x=dataset.x_axis,
                       y=dataset.y_axis)
        plt.show()

    def surface_plot(self):

        # Tworzenie wykresu
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        color_maps = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                      'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                      'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']

        cm_index = 0

        for dataset in self.__datasets.datasets:
            x = np.array(dataset.x_axis)
            y = np.array(dataset.y_axis)
            z = np.array(dataset.z_axis)

            # Tworzenie siatki dla danych
            X, Y = np.meshgrid(x, y)
            Z = np.zeros_like(X)

            for i in range(0, len(x) - 1):
                for j in range(0, len(y) - 1):
                    Z[j, i] = z[i]

            # Tworzenie heatmapy 3D
            ax.plot_surface(X, Y, Z, cmap=color_maps[cm_index], alpha=.7)

            # Ustawienie etykiet osi
            ax.set_xlabel(self.__plot_options.x_axis)
            ax.set_ylabel(self.__plot_options.y_axis)
            ax.set_zlabel(self.__plot_options.z_axis)
            cm_index += 1
        plt.show()

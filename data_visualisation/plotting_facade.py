import numpy as np
from matplotlib import pyplot as plt

from data_unification._utils import build_multiple_datasets, build_multiple_datasets_3d
from data_visualisation._implementations.manual_plots import ManualPlot
from data_visualisation._implementations.multiple_plots import MultiplePlot
from data_visualisation._implementations.heatmap import Heatmap
from data_visualisation.models import PlotOptions, FigureOptions
from data_visualisation.definitions import FigureBuilder


class PlottingFacade:
    _manual_plot = ManualPlot()
    _multiple_plot = MultiplePlot()
    _heat_map = Heatmap()

    @staticmethod
    def manual_plot():
        return PlottingFacade._manual_plot

    @staticmethod
    def multiple_plot():
        return PlottingFacade._multiple_plot

    @staticmethod
    def heatmap():
        return PlottingFacade._heat_map


class Plots2D:
    figure_builder = FigureBuilder()

    def __init__(self, data_from_db, plot_options: PlotOptions):
        self.__plot_options = plot_options
        self.__datasets = build_multiple_datasets(
            data_from_db=data_from_db,
            data_to_x_axis=plot_options.x_axis_label,
            data_to_y_axis=plot_options.y_axis_label
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


class Plots3D:
    figure_builder = FigureBuilder()

    def __init__(self, data_from_db, plot_options: FigureOptions):
        self.__plot_options = plot_options
        self.__datasets = build_multiple_datasets_3d(
            data_from_db=data_from_db,
            data_to_x_axis=plot_options.x_axis_label,
            data_to_y_axis=plot_options.y_axis_label,
            data_to_z_axis=plot_options.z_axis_label
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
            ax.set_xlabel(self.__plot_options.x_axis_label)
            ax.set_ylabel(self.__plot_options.y_axis_label)
            ax.set_zlabel(self.__plot_options.z_axis_label)
            cm_index += 1
        plt.show()

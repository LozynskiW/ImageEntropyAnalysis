import numpy as np
from matplotlib import pyplot as plt

from data_visualisation.definitions import FigureBuilder, ManualPlotDefinition, ManualPlotWithErrorsMarkersDefinition
from data_visualisation.models import PlotOptions, FigureOptions, PlotOptionsWithOYErrors


class ManualPlot(ManualPlotDefinition):
    figure_builder = FigureBuilder()

    def add_data(self, plot_options: PlotOptions):

        if plot_options.take_nth_value > 1:

            x_limited = []
            y_limited = []
            z_limited = []
            for i in range(len(plot_options.x)):
                if i % plot_options.take_nth_value == 0:
                    x_limited.append(plot_options.x[i])
                    y_limited.append(plot_options.y[i])
                    if plot_options.z is not None: z_limited.append(plot_options.z[i])

            plot_options.x = x_limited
            plot_options.y = y_limited
            plot_options.z = z_limited

    @staticmethod
    def scatter_plot(plot_options: PlotOptions, figure_options: FigureOptions = FigureOptions()):

        fig, ax = ManualPlot._build_figure(figure_options)

        ax.scatter(plot_options.x, plot_options.y, c=plot_options.color, marker=plot_options.marker)
        ax.grid()

        plt.show()

    @staticmethod
    def bar_plot(plot_options: PlotOptions, figure_options: FigureOptions = FigureOptions()):

        fig, ax = ManualPlot._build_figure(figure_options)

        ax.bar(plot_options.x, plot_options.y, plot_options.color)
        ax.grid()

        plt.show()

    @staticmethod
    def _build_figure(figure_options: FigureOptions):

        fig, ax = plt.subplots()
        fig.suptitle(figure_options.title, size=figure_options.font_size.big_font)

        ax.set_xlabel(figure_options.x_axis_label)
        ax.set_ylabel(figure_options.y_axis_label)
        ax.grid()

        return fig, ax


class ManualPlotWithErrorsMarkers(ManualPlotWithErrorsMarkersDefinition):

    def add_data(self, plot_options: PlotOptionsWithOYErrors):

        self._manual_plot.add_data(plot_options.plot_options)

        div = plot_options.plot_options.take_nth_value
        plot_options_x = plot_options.plot_options.x

        if div > 1:

            x_errors_limited = []
            y_errors_limited = []

            if not plot_options.x_errors:
                plot_options.x_errors = list(np.zeros(len(plot_options.y_errors)))

            for i in range(len(plot_options.y_errors)):
                if i % div == 0:
                    x_errors_limited.append(plot_options.x_errors[i])
                    y_errors_limited.append(plot_options.y_errors[i])

            plot_options.x_errors = x_errors_limited
            plot_options.y_errors = y_errors_limited
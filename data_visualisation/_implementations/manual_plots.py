from matplotlib import pyplot as plt

from data_visualisation.definitions import FigureBuilder
from data_visualisation.models import PlotOptions, FigureOptions


class ManualPlot:
    figure_builder = FigureBuilder()

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

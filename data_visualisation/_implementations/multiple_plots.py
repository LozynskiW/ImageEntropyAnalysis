from matplotlib import pyplot as plt

from data_visualisation._implementations.manual_plots import ManualPlot, ManualPlotWithErrorsMarkers
from data_visualisation.definitions import FigureBuilder, ManualPlotDefinition
from data_visualisation.models import PlotOptions, FigureOptions, PlotOptionsWithOYErrors


class MultiplePlot:
    figure_builder = FigureBuilder()

    @staticmethod
    def scatter_plot(figure_options: FigureOptions):
        return MultiplePlot.ScatterPlot(figure_options)

    @staticmethod
    def line_plot(figure_options: FigureOptions):
        return MultiplePlot.LinePlot(figure_options)

    @staticmethod
    def bar_plot(figure_options: FigureOptions):
        return MultiplePlot.BarPlot(figure_options)

    @staticmethod
    def scatter_with_errors_plot(figure_options: FigureOptions):
        return MultiplePlot.ScatterWithErrors(figure_options, MultiplePlot.scatter_plot(figure_options))

    class ScatterPlot(ManualPlot):
        def __init__(self, figure_options: FigureOptions):
            self._fig, self._ax = ManualPlot._build_figure(figure_options)

        def add_data(self, plot_options: PlotOptions):
            super().add_data(plot_options)
            self._ax.scatter(plot_options.x, plot_options.y, c=plot_options.color, marker=plot_options.marker,
                             label=plot_options.label)

        def show(self):
            plt.legend()
            plt.show()

        def save_to_file(self, file_name: str, dpi: int):
            plt.legend()
            plt.savefig(fname=file_name, dpi=dpi)

    class LinePlot(ManualPlot):

        def __init__(self, figure_options: FigureOptions):
            self._fig, self._ax = ManualPlot._build_figure(figure_options)

        def add_data(self, plot_options: PlotOptions):
            super().add_data(plot_options)
            self._ax.plot(plot_options.x, plot_options.y, c=plot_options.color, marker=plot_options.marker,
                          label=plot_options.label)

        def show(self):
            plt.legend()
            plt.show()

        def save_to_file(self, file_name: str, dpi: int):
            plt.legend()
            plt.savefig(fname=file_name, dpi=dpi)

    class BarPlot(ManualPlot):

        def __init__(self, figure_options: FigureOptions):
            self._fig, self._ax = ManualPlot._build_figure(figure_options)

        def add_data(self, plot_options: PlotOptions):
            super().add_data(plot_options)
            self._ax.bar(plot_options.x, plot_options.y, color=plot_options.color, label=plot_options.label)

        def show(self):
            plt.legend()
            plt.show()

        def save_to_file(self, file_name: str, dpi: int):
            plt.legend()
            plt.savefig(fname=file_name, dpi=dpi)

    class ScatterWithErrors(ManualPlotWithErrorsMarkers):

        def __init__(self, figure_options: FigureOptions, manual_plot: ManualPlotDefinition):
            super().__init__(manual_plot)
            self._fig, self._ax = ManualPlotWithErrorsMarkers._build_figure(figure_options)

        def add_data(self, plot_options: PlotOptionsWithOYErrors):
            super().add_data(plot_options)

            x = plot_options.plot_options.x
            y = plot_options.plot_options.y

            if plot_options.y_errors is None or len(plot_options.y_errors) == 0:
                self._ax.plot(x, y, c=plot_options.plot_options.color, marker=plot_options.plot_options.marker,
                                 label=plot_options.plot_options.label)
            else:
                self._ax.errorbar(x, y, yerr=plot_options.y_errors,
                                  marker=plot_options.plot_options.marker, markersize=8,
                                  linestyle='none')

        def show(self):
            plt.legend()
            plt.show()

        def save_to_file(self, file_name: str, dpi: int):
            plt.legend()
            plt.savefig(fname=file_name, dpi=dpi)
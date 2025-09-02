from matplotlib import pyplot as plt

from data_visualisation._implementations.manual_plots import ManualPlot
from data_visualisation.definitions import FigureBuilder
from data_visualisation.models import PlotOptions, FigureOptions


class MultiplePlot:
    figure_builder = FigureBuilder()

    @staticmethod
    def scatter_plot(figure_options: FigureOptions):
        return MultiplePlot.ScatterPlot(figure_options)

    class ScatterPlot(ManualPlot):
        def __init__(self, figure_options: FigureOptions):
            self._fig, self._ax = ManualPlot._build_figure(figure_options)

        def add_data(self, plot_options: PlotOptions):
            self._ax.scatter(plot_options.x, plot_options.y, c=plot_options.color, marker=plot_options.marker,
                             label=plot_options.label)

        def show(self):
            plt.legend()
            plt.show()

        def save_to_file(self, file_name: str, dpi: int):
            plt.legend()
            plt.savefig(fname=file_name, dpi=dpi)

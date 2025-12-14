import numpy as np
from matplotlib import pyplot as plt

from data_visualisation.models import PlotOptions, FigureOptions, PlotOptionsWithOYErrors


class MultiplePlot:
    _fig = None
    _ax = None
    _figure_options: FigureOptions = None

    def configure(self, figure_options: FigureOptions):
        self._fig, self._ax = self._build_figure(figure_options)
        self._figure_options = figure_options

    def clear(self):
        self._fig, self._ax = self._build_figure(self._figure_options)

    @staticmethod
    def _build_figure(figure_options: FigureOptions):

        fig, ax = plt.subplots()
        fig.suptitle(figure_options.title, size=figure_options.font_size.big_font)

        ax.set_xlabel(figure_options.x_axis_label)
        ax.set_ylabel(figure_options.y_axis_label)
        ax.grid()

        return fig, ax

    @staticmethod
    def show():
        plt.legend()
        plt.show()

    @staticmethod
    def save_to_file(file_name: str, dpi: int):
        plt.legend()
        plt.savefig(fname=file_name, dpi=dpi)

    def add_scatter_plot(self, plot_options: PlotOptions):
        self._ax.scatter(plot_options.x, plot_options.y,
                         c=plot_options.color,
                         marker=plot_options.marker,
                         label=plot_options.label)

    def add_line_plot(self, plot_options: PlotOptions):
        self._ax.plot(plot_options.x, plot_options.y,
                      c=plot_options.color,
                      # marker=plot_options.marker,
                      label=plot_options.label)

    def add_bar_plot(self, plot_options: PlotOptions):
        self._ax.bar(plot_options.x, plot_options.y,
                     color=plot_options.color,
                     label=plot_options.label)

    def add_scatter_with_errors_plot(self, plot_options: PlotOptionsWithOYErrors):
        x = plot_options.plot_options.x
        y = plot_options.plot_options.y

        if plot_options.y_errors is None or len(plot_options.y_errors) == 0:
            self.add_scatter_plot(plot_options.plot_options)
        else:
            self._ax.errorbar(x, y, yerr=plot_options.y_errors,
                              marker=plot_options.plot_options.marker, markersize=8,
                              linestyle='none')

    def add_line_with_errors_plot(self, plot_options: PlotOptionsWithOYErrors):
        x = plot_options.plot_options.x
        y = plot_options.plot_options.y

        self.add_line_plot(plot_options.plot_options)
        if len(plot_options.y_errors) > 0:
            self._ax.fill_between(x, np.add(y, plot_options.y_errors), np.subtract(y, plot_options.y_errors),
                                  color=plot_options.errors_color, alpha=.5, linewidth=0)

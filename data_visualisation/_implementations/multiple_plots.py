import numpy as np
from matplotlib import pyplot as plt

from data_visualisation.models import PlotOptions, FigureOptions, PlotOptionsWithOYErrors


class MultiplePlot:
    _fig = None
    _ax = None
    _figure_options: FigureOptions = None

    def configure(self, figure_options: FigureOptions):
        if self._fig is None or self._ax is None:
            self._fig, self._ax = self._build_new_figure(figure_options)
        else:
            self._configure_existing_figure(self._fig, self._ax, figure_options)
        self._figure_options = figure_options

    def clear(self):
        self._fig, self._ax = self._build_new_figure(self._figure_options)

    def get_ax(self):
        return self._ax

    @staticmethod
    def _build_new_figure(figure_options: FigureOptions):

        fig = plt.figure(figsize=figure_options.figure_size)
        ax = fig.add_subplot(1, 1, 1)
        MultiplePlot._configure_existing_figure(fig, ax, figure_options)
        ax.grid()

        return fig, ax

    @staticmethod
    def _configure_existing_figure(fig, ax, figure_options: FigureOptions):
        fig.suptitle(figure_options.title, size=figure_options.font_size.big_font)
        ax.set_xlabel(figure_options.x_axis_label, fontsize=20)
        ax.set_ylabel(figure_options.y_axis_label, fontsize=20)

    @staticmethod
    def show():
        plt.legend(shadow=True, fancybox=True, fontsize=14)
        plt.show()

    @staticmethod
    def save_to_file(file_name: str, dpi: int):
        plt.legend()
        plt.savefig(fname=file_name, dpi=dpi)

    def add_scatter_plot(self, plot_options: PlotOptions):
        self._ax.scatter(plot_options.x, plot_options.y,
                         c=plot_options.color,
                         marker=plot_options.marker,
                         label=plot_options.label,
                         s=plot_options.marker_size)

    def add_line_plot(self, plot_options: PlotOptions):
        self._ax.plot(plot_options.x, plot_options.y,
                      c=plot_options.color,
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


class Subplots:

    def __init__(self, figure_options: FigureOptions):
        self._fig, self._axs = self._build_new_figure(figure_options)

        self._figure_options = figure_options
        self._rows_first = figure_options.rows_first

        self._plots_grid = list(np.zeros(shape=(self._figure_options.plots_rows, self._figure_options.plots_cols)))
        self._current_ax_row = 0
        self._current_ax_col = 0

        dummy_plot = MultiplePlot()
        dummy_plot.configure(FigureOptions())
        dummy_plot.add_scatter_plot(PlotOptions(x=[], y=[], label=""))
        self.add_next_plot(dummy_plot)

    def add_next_plot(self, plot: MultiplePlot):
        if sum(sum(self._plots_grid)) == self._figure_options.plots_rows * self._figure_options.plots_cols:
            raise ValueError("all slots for plots already used")

        ax = self._get_next_ax()
        plot._ax = ax
        plot._fig = ax.figure

    def _get_next_ax(self):
        row, col = self._current_ax_row, self._current_ax_col
        ax = self._axs[row, col]

        if self._rows_first:
            # left to right
            if col + 1 < self._figure_options.plots_cols:
                self._current_ax_col += 1
            else:
                self._current_ax_col = 0
                self._current_ax_row += 1
        else:
            # top to bottom
            if row + 1 < self._figure_options.plots_rows:
                self._current_ax_row += 1
            else:
                self._current_ax_row = 0
                self._current_ax_col += 1
        return ax

    @staticmethod
    def _build_new_figure(figure_options: FigureOptions):
        fig, axs = plt.subplots(
            nrows=figure_options.plots_rows,
            ncols=figure_options.plots_cols,
            figsize=figure_options.figure_size,
            layout='constrained'
        )

        return fig, axs

    def show(self):
        plt.legend()
        plt.show()
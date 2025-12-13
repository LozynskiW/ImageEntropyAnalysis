from matplotlib import pyplot as plt

from data_visualisation.models import PlotFontSize, PlotOptions, FigureOptions


class FigureBuilder:

    def __init__(self):
        self.__ax = None

        self.set_fig_size()

    def build(self):
        return self.__ax

    def set_fig_size(self, figsize=(4, 3), dpi=200):
        fig = plt.figure(figsize=figsize, dpi=dpi)

        ax = fig.add_subplot(111)

        self.__ax = ax

    def set_font_sizes(self, plotFontSize: PlotFontSize):
        self.__ax.rc('xtick', labelsize=plotFontSize.small_font)
        self.__ax.rc('ytick', labelsize=plotFontSize.small_font)
        self.__ax.rc('legend', fontsize=plotFontSize.small_font)

        self.__ax.rc('font', size=plotFontSize.mid_font)
        self.__ax.rc('axes', titlesize=plotFontSize.mid_font)

        self.__ax.rc('figure', titlesize=plotFontSize.big_font)


class ManualPlotDefinition:

    def add_data(self, plot_options: PlotOptions):
        raise NotImplementedError

    @staticmethod
    def _build_figure(figure_options: FigureOptions):
        fig, ax = plt.subplots()
        fig.suptitle(figure_options.title, size=figure_options.font_size.big_font)

        ax.set_xlabel(figure_options.x_axis_label)
        ax.set_ylabel(figure_options.y_axis_label)
        ax.grid()

        return fig, ax


class ManualPlotWithErrorsMarkersDefinition(ManualPlotDefinition):
    _manual_plot: ManualPlotDefinition

    def __init__(self, manual_plot: ManualPlotDefinition):
        self._manual_plot = manual_plot

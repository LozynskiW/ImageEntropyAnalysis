from matplotlib import pyplot as plt


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

    def set_font_sizes(self, small_size=12, medium_size=16, big_size=20):

        self.__ax.rc('xtick', labelsize=small_size)  # fontsize of the tick labels
        self.__ax.rc('ytick', labelsize=small_size)  # fontsize of the tick labels
        self.__ax.rc('legend', fontsize=small_size)  # legend fontsize

        self.__ax.rc('font', size=medium_size)  # controls default text sizes
        self.__ax.rc('axes', titlesize=medium_size)  # fontsize of the axes title

        self.__ax.rc('figure', titlesize=big_size)  # fontsize of the figure title
from matplotlib import pyplot as plt
from app.data_visualisation.util.figure_and_plot_style import FigureBuilder


def scatter_plot(data_to_plot, figure_builder=FigureBuilder(), style={}):

    figure = figure_builder.build()

    for dataset in data_to_plot.keys():

        figure.scatter(data_to_plot[dataset]["ox"], data_to_plot[dataset]["oy"])

    plt.show()


def line_plot(self, ox_label="X", oy_label="Y"):
    plt.figure(figsize=(16, 9), dpi=180)

    plt.xlabel(ox_label)
    plt.ylabel(oy_label)

    plt.plot(self.__ox, self.__oy)

    plt.grid()
    plt.show()


def scatter_plot_3d(self, ox_label="X", oy_label="Y", oz_label="Z"):
    fig = plt.figure(figsize=(16, 9), dpi=180)

    ax = fig.add_subplot(projection='3d')

    ax.scatter(self.__ox, self.__oy, self.__oz)

    ax.set_xlabel(ox_label)
    ax.set_ylabel(oy_label)
    ax.set_zlabel(oz_label)

    plt.grid()
    plt.show()


def bar_plot(self, ox_label="X", oy_label="Y"):
    plt.figure(figsize=(16, 9), dpi=180)
    plt.bar(self.__ox, self.__oy)
    plt.xlabel(ox_label)
    plt.ylabel(oy_label)
    plt.grid()
    plt.show()
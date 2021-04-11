from matplotlib import pyplot as plt
import numpy as np


class DBdataProcessor:
    def __init__(self):
        self.__ox = []
        self.__oy = []
        self.__sort_spans = []

    def get_data_with_respect_to(self, data, ox, oy):
        self.__ox = [float(x[ox]) for x in data]
        self.__oy = [float(y[oy]) for y in data]

    def sort_spans_for_angles(self):
        for i in range(-17, 18):
            self.__sort_spans.append([(i-1)*10, i*10])

        self.__ox = [[] for i in range(0, len(self.__sort_spans))]
        self.__oy = self.__ox.copy()

    def plot(self, plot_type='line', ox_label='X', oy_label='Y'):
        if plot_type == 'line':
            self.__line_plot(ox_label, oy_label)
        if plot_type == 'scatter':
            self.__scatter_plot(ox_label, oy_label)
        if plot_type == 'bar':
            self.__bar_plot(ox_label, oy_label)

    def __line_plot(self, ox_label="X", oy_label="Y"):
        plt.figure()
        plt.plot(self.__ox, self.__oy)
        plt.xlabel(ox_label)
        plt.ylabel(oy_label)
        plt.grid()
        plt.show()

    def __scatter_plot(self, ox_label="X", oy_label="Y"):
        plt.figure()
        plt.scatter(self.__ox, self.__oy)
        plt.xlabel(ox_label)
        plt.ylabel(oy_label)
        plt.grid()
        plt.show()

    def __bar_plot(self, ox_label="X", oy_label="Y"):
        plt.figure()
        plt.bar(self.__ox, self.__oy)
        plt.xlabel(ox_label)
        plt.ylabel(oy_label)
        plt.grid()
        plt.show()


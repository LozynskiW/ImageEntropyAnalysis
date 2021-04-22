import datetime
from datetime import time

from matplotlib import pyplot as plt
import numpy as np


class DBdataProcessor:
    def __init__(self):
        self.__ox = []
        self.__oy = []
        self.__ox_per_dataset = []
        self.__oy_per_dataset = []
        self.__sort_spans = []

    def get_data_with_respect_to(self, data, ox, oy):
        self.__ox = [x[ox] for x in data]
        self.__oy = [y[oy] for y in data]

    def sort_spans_for_angles(self):
        for i in range(-17, 18):
            self.__sort_spans.append([(i - 1) * 10, i * 10])

        self.__ox = [[] for i in range(0, len(self.__sort_spans))]
        self.__oy = self.__ox.copy()

    def group_data_by_dataset(self, data, ox, oy):
        datasets = self.__select_datasets(data)
        self.__ox_per_dataset = []
        self.__oy_per_dataset = []
        for d in datasets:
            temp = self.__filtering(data, d)
            self.get_data_with_respect_to(temp, ox, oy)
            if ox == 'time':
                for i in range(0, len(self.__ox)):
                    self.__ox[i] = datetime.datetime.strptime(self.__ox[i], '%Y:%m:%d:%H:%M:%S')
                    #self.__ox[i] = time(self.__ox[i].hour, self.__ox[i].minute)
                    self.__ox[i] = self.__ox[i].hour
            self.__ox_per_dataset.append(self.__ox)
            self.__oy_per_dataset.append(self.__oy)

        self.__multiple_scatter_plot(ox_label=ox, oy_label=oy, legend=datasets)

    def plot(self, plot_type='line', ox_label='X', oy_label='Y'):
        if plot_type == 'line':
            self.__line_plot(ox_label, oy_label)
        if plot_type == 'scatter':
            self.__scatter_plot(ox_label, oy_label)
        if plot_type == 'bar':
            self.__bar_plot(ox_label, oy_label)

    def __multiple_scatter_plot(self, ox_label=None, oy_label=None, legend=None):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        for i in range(0, len(self.__ox_per_dataset)):
            print(i, len(legend), len(self.__ox_per_dataset))
            ax.scatter(self.__ox_per_dataset[i], self.__oy_per_dataset[i], label=legend[i])
            plt.ylim(bottom=0)
            #ax.axes.xaxis.set_visible(False)

        if legend is not None:
            plt.legend(loc='upper right')

        if ox_label is not None:
            plt.xlabel(ox_label)
        if oy_label is not None:
            plt.ylabel(oy_label)
        plt.grid()
        plt.show()

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

    @staticmethod
    def __filtering(data, dataset):
        out = []
        for d in data:
            if d['dataset'] == dataset:
                out.append(d)
        return out

    @staticmethod
    def __select_datasets(data):
        datasets = []

        for d in data:
            if d['dataset'] not in datasets:
                datasets.append(d['dataset'])

        return datasets


import datetime
import os
from numpy import mean, max

from matplotlib import pyplot as plt


class DBdataProcessor:
    def __init__(self):
        self.__ox = []
        self.__oy = []
        self.__ox_per_dataset = []
        self.__oy_per_dataset = []
        self.__sort_spans = []
        self.__def_figure_folder = "figures/"

    def get_data_with_respect_to(self, data, ox, oy):
        self.__ox = [x[ox] for x in data]
        self.__oy = [y[oy] for y in data]

    def sort_spans_for_angles(self):
        for i in range(-17, 18):
            self.__sort_spans.append([(i - 1) * 10, i * 10])

        self.__ox = [[] for i in range(0, len(self.__sort_spans))]
        self.__oy = self.__ox.copy()

    def group_and_plot_data_by_object_class(self, data, oy, mean):

        objects = self.__select_objects(data)
        self.__ox_per_dataset = []
        self.__oy_per_dataset = []

        self.get_data_with_respect_to(data, 'object', oy)

        for o in objects:
            """[[daniel][dzik][sarna][zajac]]"""
            object_data = self.__filter_by_value(data=data, pool_to_filter='object', value_to_filter=o)
            """[daniel]"""
            if oy == 'histogram':
                self.__oy = list(map(lambda x: x[oy]['data'], object_data))  # [wskazany parametr tylko dla daniela]
                self.__oy = self.__mean_of_histogram(self.__oy)
            else:
                self.__oy = list(map(lambda x: x[oy], object_data))  # [wskazany parametr tylko dla daniela]

            self.__ox_per_dataset.append(list(filter(lambda x: x == o, self.__ox)))  # [daniel, daniel, daniel...]
            self.__oy_per_dataset.append(self.__oy)

        self.__multiple_scatter_plot(ox_label='classes_of_objects', oy_label=oy, legend=None, plot_mean=mean)

    def group_data_by_dataset(self, data, ox, oy):
        datasets = self.__select_datasets(data)
        self.__ox_per_dataset = []
        self.__oy_per_dataset = []
        for d in datasets:
            temp = self.__filter_by_dataset(data, d)
            self.get_data_with_respect_to(temp, ox, oy)
            if ox == 'time':
                for i in range(0, len(self.__ox)):
                    self.__ox[i] = datetime.datetime.strptime(self.__ox[i], '%Y:%m:%d:%H:%M:%S')
                    # self.__ox[i] = time(self.__ox[i].hour, self.__ox[i].minute)
                    self.__ox[i] = self.__ox[i].hour
            self.__ox_per_dataset.append(self.__ox)
            self.__oy_per_dataset.append(self.__oy)

        # self.__multiple_scatter_plot(ox_label=ox, oy_label=oy, legend=datasets)

    def plot_whole_dataset(self, data, ox, oy, mode, filename):

        datasets = self.__select_datasets(data)

        self.group_data_by_dataset(data, ox, oy)

        self.__multiple_scatter_plot(ox_label=ox, oy_label=oy, legend=datasets, mode=mode, filename=filename)

    def plot(self, plot_type='line', ox_label='X', oy_label='Y'):

        if plot_type == 'line':
            self.__line_plot(ox_label, oy_label)
        if plot_type == 'scatter':
            self.__scatter_plot(ox_label, oy_label)
        if plot_type == 'bar':
            self.__bar_plot(ox_label, oy_label)

    def __multiple_scatter_plot(self, ox_label=None, oy_label=None, legend=None, mode=None, filename="default",
                                plot_mean='off'):

        if mode is None:
            mode = "show"

        fig = plt.figure(figsize=(16, 9), dpi=180)
        ax = fig.add_subplot(111)

        SMALL_SIZE = 16
        MEDIUM_SIZE = 20
        BIGGER_SIZE = 12

        plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
        plt.rc('axes', titlesize=MEDIUM_SIZE)  # fontsize of the axes title
        plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

        for i in range(0, len(self.__ox_per_dataset)):
            if legend is not None:
                ax.scatter(self.__ox_per_dataset[i], self.__oy_per_dataset[i], label=legend[i])
            else:
                ax.scatter(self.__ox_per_dataset[i], self.__oy_per_dataset[i])
            y_top_lim = max(list(map(lambda a: max(a), self.__oy_per_dataset)))
            y_bot_lim = min(list(map(lambda a: max(a), self.__oy_per_dataset)))
            plt.ylim(bottom=0, top=y_top_lim + 0.1 * y_top_lim)
            """plt.subplots_adjust(top=1, bottom=0.08, right=0.99, left=0.06,
                                hspace=0, wspace=0)"""
            if plot_mean == 'on':
                ax.scatter(self.__ox_per_dataset[i][0], mean(self.__oy_per_dataset[i]), 200, color='black')

        if legend is not None:
            plt.legend(loc='upper right')

        if ox_label is not None:
            plt.xlabel(ox_label, labelpad=15)

        if oy_label is not None:
            plt.ylabel(oy_label, labelpad=15)

        plt.grid()

        if mode == "show":
            plt.show()

        if mode == "save":

            fig_name = filename + "_" + ox_label + "_" + oy_label + ".png"

            if not os.path.exists(self.__def_figure_folder + '/' + filename):
                # Create target Directory
                os.mkdir(self.__def_figure_folder + '/' + filename)

            plt.savefig(self.__def_figure_folder + '/' + filename + '/' + fig_name)
            print(fig_name, 'saved to', self.__def_figure_folder + filename)

        plt.close(fig=fig)

    def __line_plot(self, ox_label="X", oy_label="Y"):
        plt.figure(figsize=(16, 9), dpi=180)
        plt.plot(self.__ox, self.__oy)
        plt.xlabel(ox_label)
        plt.ylabel(oy_label)
        plt.grid()
        plt.show()

    def __scatter_plot(self, ox_label="X", oy_label="Y"):
        plt.figure(figsize=(16, 9), dpi=180)
        plt.scatter(self.__ox, self.__oy)
        plt.xlabel(ox_label)
        plt.ylabel(oy_label)
        plt.grid()
        plt.show()

    def __bar_plot(self, ox_label="X", oy_label="Y"):
        plt.figure(figsize=(16, 9), dpi=180)
        plt.bar(self.__ox, self.__oy)
        plt.xlabel(ox_label)
        plt.ylabel(oy_label)
        plt.grid()
        plt.show()

    @staticmethod
    def __filter_by_dataset(data, dataset):
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

    @staticmethod
    def __select_objects(data):
        objects = []

        for d in data:
            if d['object'] not in objects:
                objects.append(d['object'])

        return objects

    @staticmethod
    def __filter_by_value(data, pool_to_filter, value_to_filter):
        return list(filter(lambda d: d[pool_to_filter] == value_to_filter, data))

    @staticmethod
    def __mean_of_histogram(histograms):
        histograms_means = []
        for h in histograms:
            mean = 0
            for i in range(0, 256):
                mean = i * h[i] + mean
            histograms_means.append(mean)
        return histograms_means

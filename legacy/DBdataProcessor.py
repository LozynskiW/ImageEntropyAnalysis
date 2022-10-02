import datetime
import os

import numpy as np
from numpy import mean, max, arctan, ceil, min

from matplotlib import pyplot as plt


class DBdataProcessor:
    def __init__(self):
        self.__ox = []
        self.__oy = []
        self.__oz = []
        self.__ox_per_dataset = []
        self.__oy_per_dataset = []
        self.__oz_per_dataset = []
        self.__sort_spans = []
        self.__def_figure_folder = "figures/"

    def set_folder_to_save_figures(self, folder_path):
        self.__def_figure_folder = folder_path

    def get_data_with_respect_to(self, data, ox=None, oy=None, oz=None):

        if ox is not None:
            ox = [x[ox] for x in data]
        else:
            ox = []

        if oy is not None:
            oy = [y[oy] for y in data]
        else:
            oy = []

        if oz is not None:
            oz = [z[oz] for z in data]
        else:
            oz = []

        return ox, oy, oz

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
        self.__oz_per_dataset = []

        for d in datasets:

            temp = self.__filter_by_dataset(data, d)

            self.__ox, self.__oy, _ = self.get_data_with_respect_to(temp, ox, oy)

            if ox == 'time':
                for i in range(0, len(self.__ox)):
                    self.__ox[i] = datetime.datetime.strptime(self.__ox[i], '%Y:%m:%d:%H:%M:%S')
                    # self.__ox[i] = time(self.__ox[i].hour, self.__ox[i].minute)
                    self.__ox[i] = self.__ox[i].hour

            self.__ox_per_dataset.append(self.__ox)
            self.__oy_per_dataset.append(self.__oy)

    def group_data_by_dataset_and_aggregate(self, data, oy, function='mean'):
        datasets = self.__select_datasets(data)
        self.__ox_per_dataset = []
        self.__oy_per_dataset = []
        self.__oz_per_dataset = []

        for d in datasets:

            temp = self.__filter_by_dataset(data, d)

            _, self.__oy, _ = self.get_data_with_respect_to(data=temp, ox=None, oy=oy)

            if function == 'mean':
                self.__oy_per_dataset.append(mean(self.__oy))
            if function == 'max':
                self.__oy_per_dataset.append(max(self.__oy))
            if function == 'min':
                self.__oy_per_dataset.append(min(self.__oy))

            self.__ox_per_dataset.append(d)

    def plot_whole_dataset(self,
                           data,
                           ox,
                           oy,
                           legend=True,
                           mode=None,
                           filename='default',
                           plot_title='',
                           translate_names_to_azimuthal_angle=False,
                           translate_datasets_to_elevation_angle=False):

        if legend:
            if not type(legend) == list:
                legend = self.__select_datasets(data)

        #self.group_data_by_dataset(data, ox, oy)

        self.group_data_by_dataset_and_aggregate(data, oy, function='mean')

        self.__multiple_scatter_plot(ox_label=ox,
                                     oy_label=oy,
                                     legend=legend,
                                     mode=mode,
                                     filename=filename,
                                     translate_names_to_azimuthal_angle=translate_names_to_azimuthal_angle,
                                     translate_datasets_to_elevation_angle=translate_datasets_to_elevation_angle,
                                     plot_title=plot_title,
                                     plot_mean='off')

    def plot(self, plot_type='line', ox_label='X', oy_label='Y'):

        if plot_type == 'line':
            self.__line_plot(ox_label, oy_label)
        if plot_type == 'scatter':
            self.__scatter_plot(ox_label, oy_label)
        if plot_type == 'bar':
            self.__bar_plot(ox_label, oy_label)

    @staticmethod
    def style_plot(plt, small_fontsize=16, medium_fontsize=20, bigger_fontsize=12):

        plt.rc('font', size=small_fontsize)  # controls default text sizes
        plt.rc('axes', titlesize=medium_fontsize)  # fontsize of the axes title
        plt.rc('xtick', labelsize=small_fontsize)  # fontsize of the tick labels
        plt.rc('ytick', labelsize=small_fontsize)  # fontsize of the tick labels
        plt.rc('legend', fontsize=small_fontsize)  # legend fontsize
        plt.rc('figure', titlesize=bigger_fontsize)  # fontsize of the figure title

        return plt


    def __multiple_scatter_plot_re(self,
                                   ox_label=None,
                                   oy_label=None,
                                   legend=None,
                                   mode='show',
                                   filename="default",
                                   plot_mean='off',
                                   translate_names_to_azimuthal_angle=False,
                                   translate_datasets_to_elevation_angle=False,
                                   plot_title='',
                                   scatter_points_size=10):

        fig = plt.figure(figsize=(4, 3), dpi=200)

        if mode == 'save':
            fig = plt.figure(figsize=(16, 9), dpi=200)

        ax = fig.add_subplot(111)


    def __multiple_scatter_plot(self,
                                ox_label=None,
                                oy_label=None,
                                legend=None,
                                mode='show',
                                filename="default",
                                plot_mean='off',
                                translate_names_to_azimuthal_angle=False,
                                translate_datasets_to_elevation_angle=False,
                                plot_title='',
                                scatter_points_size=10):

        fig = plt.figure(figsize=(4, 3), dpi=200)

        if mode == 'save':
            fig = plt.figure(figsize=(16, 9), dpi=200)

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

        legend_title = 'Datasets'

        if translate_datasets_to_elevation_angle:
            legend_title = "Elevation angle in deg"
            self.__ox_per_dataset = self.__translate_datasets_names_to_deg(legend)

        for i in range(0, len(self.__ox_per_dataset)):

            x = self.__ox_per_dataset[i]

            if translate_names_to_azimuthal_angle:
                x = self.__translate_imgs_names_to_deg(x)
                ax.set_xticks(np.arange(0, 361, 30.0))

            if legend is not None:
                ax.scatter(x, self.__oy_per_dataset[i], label=legend[i], s=scatter_points_size)
            else:
                ax.scatter(x, self.__oy_per_dataset[i], s=scatter_points_size)

            y_top_lim = max(list(map(lambda a: max(a), self.__oy_per_dataset)))
            y_bot_lim = min(list(map(lambda a: max(a), self.__oy_per_dataset)))

            plt.ylim(bottom=0, top=y_top_lim + 0.1 * y_top_lim)

            if plot_mean == 'on':
                ax.scatter(self.__ox_per_dataset[i][0], mean(self.__oy_per_dataset[i]), 200, color='black')

        if legend is not None:
            lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=legend_title, markerscale=5.0)

        if ox_label is not None:
            if translate_names_to_azimuthal_angle:
                plt.xlabel('azimuthal_angle', labelpad=15)
            else:
                plt.xlabel(ox_label, labelpad=15)

        if oy_label is not None:
            plt.ylabel(oy_label, labelpad=15)

        fig.subplots_adjust(right=0.75)
        plt.title(plot_title)
        plt.grid()
        plt.draw()

        if mode == "show":
            plt.show()

        if mode == "save":

            fig_name = filename + "_" + ox_label + "_" + oy_label + ".png"

            if not os.path.exists(self.__def_figure_folder):
                # Create target Directory
                os.mkdir(self.__def_figure_folder)

            plt.savefig(self.__def_figure_folder + fig_name,
                        orientation='landscape')
            print(fig_name, 'saved to', self.__def_figure_folder+fig_name)

            plt.close(fig=fig)

    def __3d_multiple_scatter_plot(self, ox_label=None, oy_label=None, oz_label=None, legend=None, mode="show",
                                   filename="default", plot_mean='off', translate_names_to_deg=False):

        fig = plt.figure(figsize=(16, 9), dpi=180)
        ax = fig.add_subplot(111, projection="3d")

        SMALL_SIZE = 16
        MEDIUM_SIZE = 20
        BIGGER_SIZE = 12

        plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
        plt.rc('axes', titlesize=MEDIUM_SIZE)  # fontsize of the axes title
        plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure

        if oy_label == 'pitch':
            new_oz_per_dataset = []

            for z in self.__oz_per_dataset:
                new_z = self.__translate_datasets_names_to_deg(z)
                new_oz_per_dataset.append(new_z)

            self.__oz_per_dataset = new_oz_per_dataset

        for i in range(0, len(self.__ox_per_dataset)):

            x = self.__ox_per_dataset[i]
            y = self.__oy_per_dataset[i]
            z = self.__oz_per_dataset[i]

            if translate_names_to_deg:
                x = self.__translate_imgs_names_to_deg(x)
            if legend is not None:
                ax.scatter(x, y, z, label=legend[i])
            else:
                ax.scatter(x, y, z)

            y_top_lim = max(list(map(lambda a: max(a), self.__oy_per_dataset)))
            y_bot_lim = min(list(map(lambda a: max(a), self.__oy_per_dataset)))
            plt.ylim(bottom=0, top=y_top_lim + 0.1 * y_top_lim)
            """plt.subplots_adjust(top=1, bottom=0.08, right=0.99, left=0.06,
                                hspace=0, wspace=0)"""

        if legend is not None:
            plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper right')
        plt.tight_layout()

        if ox_label is not None:
            if translate_names_to_deg:
                plt.xlabel('azimuthal angle', labelpad=15)
            else:
                plt.xlabel(ox_label, labelpad=15)

        if oy_label is not None:
            plt.ylabel(oy_label, labelpad=15)

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

        plt.xlabel(ox_label)
        plt.ylabel(oy_label)

        plt.scatter(self.__ox, self.__oy)

        plt.grid()
        plt.show()

    def __3d_scatter_plot(self, ox_label="X", oy_label="Y", oz_label="Z"):
        fig = plt.figure(figsize=(16, 9), dpi=180)

        ax = fig.add_subplot(projection='3d')

        ax.scatter(self.__ox, self.__oy, self.__oz)

        ax.set_xlabel(ox_label)
        ax.set_ylabel(oy_label)
        ax.set_zlabel(oz_label)

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

    @staticmethod
    def __translate_imgs_names_to_deg(data):

        try:
            names = [x['file'] for x in data]
        except:
            names = data

        names_deg = []

        deg_for_fps = 360 / len(names)

        for name in names:
            name = name.split('.')[0]

            names_deg.append(int(name) * deg_for_fps)

        return names_deg

    @staticmethod
    def __translate_datasets_names_to_deg(datasets):

        names_deg = []

        for dataset in datasets:
            height = dataset.split('_')[0]
            radius = dataset.split('_')[1]

            height = height.replace('h', '')
            height = float(height.replace('m', ''))
            radius = radius.replace('r', '')
            radius = float(radius.replace('m', ''))

            names_deg.append(str(round(arctan(radius/height)*(180/3.1415))))

        return names_deg
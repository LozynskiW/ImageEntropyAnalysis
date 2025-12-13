import math

import matplotlib
import numpy as np

from data_visualisation.models import PlotOptions, FigureOptions, PlotColor
from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_visualisation.plotting_facade import PlottingFacade
from matplotlib import pyplot as plt


def create_bins(min_value, max_value, step) -> np.ndarray:
    return np.arange(start=min_value, stop=max_value + 1, step=step, dtype=int)


def calculate_counts_for_bins(histogram: list | np.ndarray, bins: list | np.ndarray, offset=0):
    counts_for_bins = np.zeros(len(bins))

    current_bin_index = 0

    for val_index in range(offset, len(histogram)):

        if val_index < bins[current_bin_index]:
            counts_for_bins[current_bin_index] += histogram[val_index]
        else:
            current_bin_index += 1

    return counts_for_bins


def distances_list(distance_x_z_list: list[tuple]) -> list[str]:
    return list(
        map(lambda x_z_tuple: str(int(math.sqrt(math.pow(x_z_tuple[0], 2) + math.pow(x_z_tuple[1], 2))))+" [m]", distance_x_z_list))


app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

objects = [
    'sphere', 'cube', 'cone', 'cylinder'
]

datasets_for_objects = [
    'white_only', 'gradient', 'white_noise'
]

x_z_coordinates_pairs = [(10, 10), (20, 20), (40, 40), (80, 80), (140, 140), (200, 200)]

grayscale_histogram_values = np.linspace(1, 255, num=254)

bins_num = 8
max_histogram_value = 256
step = int(max_histogram_value / bins_num)
bins_for_histogram = create_bins(min_value=step, max_value=max_histogram_value, step=step)

figure_options = FigureOptions(
        x_axis_label="histogram bin",
        y_axis_label="number of pixels in bin"
)

for obj in objects:
    app_manager.set_object(object=obj)

    for dataset in datasets_for_objects:
        multiple_plot = PlottingFacade.multiple_plot().bar_plot(figure_options)

        data_for_obj = (app_manager
                        .load_data_from_db()
                        .custom_data({"dataset": dataset}))

        histogram_data = np.zeros(len(bins_for_histogram))

        for data_for_image in data_for_obj:

            x = data_for_image["x"]
            z = data_for_image["z"]

            if not (x, z) in x_z_coordinates_pairs:
                continue

            histogram = data_for_image["histogram_of_processed_image"]

            bins_counts = calculate_counts_for_bins(histogram, bins_for_histogram, offset=1)

            for x_val_index in range(0, len(bins_counts)):
                histogram_data[x_val_index] = bins_counts[x_val_index]

            plot_options = PlotOptions(
                x=list(bins_for_histogram),
                y=list(bins_counts),
                label=f'{dataset}'
            )
            multiple_plot.add_data(plot_options)

        multiple_plot.show()


import math

import numpy as np

from application_management.app import AppManager
from data_visualisation._implementations.heatmap import HeatmapConfig
from data_visualisation.models import FigureOptions
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_visualisation.plotting_facade import PlottingFacade
from examples.utils import ALL_OBJECTS_LIST, ALL_DATASETS_LIST
from image_processing.basictools.statisticalparameters import information_entropy_for_histogram, normalize_histogram, \
    std_dev_from_histogram

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

grayscale_histogram_values = np.linspace(1, 255, num=254)

inf_entropy_fun = lambda x: information_entropy_for_histogram(
        histogram_values=grayscale_histogram_values,
        histogram_probabilities=normalize_histogram(x["histogram_of_processed_image"][1:]))

bits_for_range_fun = lambda x: information_entropy_for_histogram(
        histogram_values=grayscale_histogram_values,
        histogram_probabilities=normalize_histogram(x["histogram_of_processed_image"][1:])) / (2*3*std_dev_from_histogram(grayscale=grayscale_histogram_values, gray_shade_prob=normalize_histogram(x["histogram_of_processed_image"][1:])))

plotted_params = {
    'H(X) / 6xσ(X)': {"func": bits_for_range_fun, "label": "bits_for_range"},
    'H(X)': {"func": inf_entropy_fun, "label": "inf_entropy"}
}

def round_down_to_tens(n):
    return math.floor(n / 10) * 10

x_axis = "z"
y_axis = "pitch"

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

for plotted_param in plotted_params.keys():
    for obj in ALL_OBJECTS_LIST:

        app_manager.set_object(object=obj)

        for dataset in ALL_DATASETS_LIST:

            data_from_db = (app_manager
                            .load_data_from_db()
                            .custom_data({"dataset": {"$in": [dataset]}}))

            for data in data_from_db:
                data[y_axis] = int(round_down_to_tens(math.degrees(math.atan2(data["x"], data["z"]))))
                data[x_axis] = int(round_down_to_tens(data["z"]))

            app_manager.set_data_from_db(data_from_db=data_from_db)

            figure_options = FigureOptions(
                x_axis_label=x_axis,
                y_axis_label=y_axis,
                z_axis_label=plotted_param,
                title=f'{obj}-{dataset}: {plotted_param}',
                figure_size=(30, 10)
            )

            heatmap_config = HeatmapConfig(
                show_cbar=False,
                show_annotations=True,
                to_percentage=False,
                values_mapping_fun=plotted_params[plotted_param]["func"],
                dpi=500
            )

            # PlottingFacade.heatmap().plot_data(
            #     data_from_db=data_from_db,
            #     figure_options=figure_options,
            #     config=heatmap_config
            # )

            PlottingFacade.heatmap().save_to_file(
                data_from_db=data_from_db,
                figure_options=figure_options,
                config=heatmap_config,
                file_name=f'{path_to_save_figures}/heatmaps_trajectory/h_pitch/{obj}_{dataset}_{plotted_params[plotted_param]["label"]}'
            )
# _bits_for_range
# _x_z
# _h_pitch
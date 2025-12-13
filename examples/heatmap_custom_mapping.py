import math

import numpy as np

from application_management.app import AppManager
from data_visualisation._implementations.heatmap import HeatmapConfig
from data_visualisation.models import FigureOptions
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_visualisation.plotting_facade import PlottingFacade
from image_processing.basictools.statisticalparameters import information_entropy_for_histogram, normalize_histogram

object_to_plot = 'cylinder' # cube sphere cone cylinder
dataset_for_objects = ['gradient']  # gradient white_noise white_only
path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

plotted_param = 'distance and pitch_angle on information_entropy_for_histogram'

grayscale_histogram_values = np.linspace(1, 255, num=254)
values_mapping_fun = lambda x: information_entropy_for_histogram(
        histogram_values=grayscale_histogram_values,
        histogram_probabilities=normalize_histogram(x["histogram_of_processed_image"][1:]))

def round_down_to_tens(n):
    return math.floor(n / 10) * 10

x_axis = "distance"
y_axis = "pitch_angle"

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)
app_manager.set_object(object=object_to_plot)

data_from_db = (app_manager
                .load_data_from_db()
                .custom_data({"dataset": {"$in": dataset_for_objects}}))

for data in data_from_db:
    data[y_axis] = int(round_down_to_tens(math.degrees(math.atan2(data["z"], data["x"]))))
    data[x_axis] = int(round_down_to_tens(math.sqrt(math.pow(data["x"], 2) + math.pow(data["z"], 2))))

app_manager.set_data_from_db(data_from_db=data_from_db)

figure_options = FigureOptions(
    x_axis_label=x_axis,
    y_axis_label=y_axis,
    z_axis_label=plotted_param,
    title=f'{object_to_plot}: {plotted_param}'
)

heatmap_config = HeatmapConfig(
    show_cbar=False,
    show_annotations=True,
    to_percentage=False,
    values_mapping_fun=values_mapping_fun,
    dpi=200
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
    file_name=f'{path_to_save_figures}/{object_to_plot}_heatmap_{dataset_for_objects}_{plotted_param}'
)

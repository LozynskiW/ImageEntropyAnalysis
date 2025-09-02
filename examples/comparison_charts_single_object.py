import math

import numpy as np

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_visualisation.models import PlotOptions, FigureOptions, PlotColor
from data_visualisation.plotting_facade import PlottingFacade
from image_processing.basictools.statisticalparameters import exp_val_from_histogram, std_dev_from_histogram, \
    information_entropy_for_histogram, normalize_histogram

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

objects = [
    'sphere', 'cube', 'cone', 'cylinder'
]

datasets_for_objects = {
    'white_only': PlotColor.RED,
    'gradient': PlotColor.GREEN,
    'white_noise': PlotColor.BLUE
}

# objects = [
#     'sphere'
# ]
#
# datasets_for_objects = {
#     'white_noise': PlotColor.RED,
#     'world_636363FF': PlotColor.GREEN,
#     'world_898989FF': PlotColor.BLUE,
#     'world_A5A5A5FF': PlotColor.YELLOW,
#     'world_BCBCBCFF': PlotColor.MAGENTA,
#     'world_CFCFCFFF': PlotColor.BLACK,
#     'world_E1E1E1FF': PlotColor.CYAN,
#     'world_F0F0F0FF': PlotColor.VIOLET
# }

plotted_params = {
    "expected_value_of_processed_image": lambda x: exp_val_from_histogram(
        grayscale=np.linspace(1, 256),
        gray_shade_prob=normalize_histogram(x["histogram_of_processed_image"][1:])),
    "standard_deviation_of_processed_image": lambda x: std_dev_from_histogram(
        grayscale=np.linspace(1, 256),
        gray_shade_prob=normalize_histogram(x["histogram_of_processed_image"][1:])),
    "entropy_in_bits_of_processed_image": lambda x: information_entropy_for_histogram(
        histogram_values=np.linspace(1, 256),
        histogram_probabilities=normalize_histogram(x["histogram_of_processed_image"][1:]))
}

for plotted_param in plotted_params:

    figure_options = FigureOptions(
        x_axis_label="distance from object [m]",
        y_axis_label=f'{plotted_param}'
    )

    for obj in objects:
        app_manager.set_object(object=obj)
        figure_options.title = obj
        multiple_plot = PlottingFacade.multiple_plot().scatter_plot(figure_options)

        for dataset in datasets_for_objects.keys():
            data_for_obj = (app_manager
                            .load_data_from_db()
                            .custom_data({"dataset": dataset}))

            plotted_param_y = list(map(plotted_params[plotted_param], data_for_obj))

            distance_x = list(map(lambda xi: math.sqrt(math.pow(xi["x"], 2) + math.pow(xi["z"], 2)), data_for_obj))

            plot_options = PlotOptions(x=distance_x, y=plotted_param_y, color=datasets_for_objects[dataset],
                                       label=f'{dataset}')
            multiple_plot.add_data(plot_options)

        # multiple_plot.save_to_file(file_name=f'{path_to_save_figures}/{obj}_{plotted_param}', dpi=200)
        multiple_plot.show()

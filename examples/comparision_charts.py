import math

from matplotlib import pyplot as plt

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_unification.enums import PersistentNames, KeyValues
from data_visualisation.labels import Label
from data_visualisation.models import PlotColor, PlotMarker
app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

objects = {
    'cube': {'color': PlotColor.BLUE, 'marker': PlotMarker.PLUS},
    'cone': {'color': PlotColor.GREEN, 'marker': PlotMarker.STAR},
    'sphere': {'color': PlotColor.MAGENTA, 'marker': PlotMarker.POINT},
    'cylinder': {'color': PlotColor.YELLOW, 'marker': PlotMarker.X}
}

datasets_for_objects = ['white_only', 'gradient', 'white_noise']

plotted_params = [
    PersistentNames.EXPECTED_VALUE_OF_PROCESSED_IMAGE,
    PersistentNames.STANDARD_DEVIATION_OF_PROCESSED_IMAGE,
    PersistentNames.ENTROPY_IN_BITS_OF_PROCESSED_IMAGE
]

for dataset_for_objects in datasets_for_objects:

    for plotted_param in plotted_params:

        fig, ax = plt.subplots(1, 1, figsize=(15, 10), layout='constrained')

        for obj in objects.keys():

            app_manager.set_object(object=obj)
            data_for_obj = (app_manager
                            .load_data_from_db()
                            .custom_data({"dataset": dataset_for_objects}))

            ax.grid(True)
            ax.set_title(f'{dataset_for_objects}', fontsize=20)
            ax.set_ylabel(f'{Label.get_symbol(plotted_param)}', fontsize=20)
            ax.set_xlabel(f'{Label.get_symbol(KeyValues.DISTANCE)}', fontsize=20)

            y = list(map(lambda yi: yi[f'{plotted_param}'], data_for_obj))

            x = list(map(lambda xi: math.sqrt(math.pow(xi["x"], 2) + math.pow(xi["z"], 2)), data_for_obj))

            ax.scatter(x, y, label=f'{obj}', color=objects[obj]['color'], marker=objects[obj]['marker'])
            ax.legend(shadow=True, fancybox=True, fontsize=20)

        plt.savefig(fname=f'{path_to_save_figures}/comparison/{dataset_for_objects}_{plotted_param}_d', dpi=200)
        # plt.show()
        plt.close(fig)

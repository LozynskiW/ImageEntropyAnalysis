import math

from matplotlib import pyplot as plt

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_unification.enums import PersistentNames
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

fig, axs = plt.subplots(3, 3, figsize=(10, 8), layout='constrained')
ax_col = 0
ax_row = 0

for dataset_for_objects in datasets_for_objects:

    ax_row = 0

    for plotted_param in plotted_params:

        for obj in objects.keys():

            app_manager.set_object(object=obj)
            data_for_obj = (app_manager
                            .load_data_from_db()
                            .custom_data({"dataset": dataset_for_objects}))

            ax = axs[ax_row, ax_col]
            ax.grid(True)
            if ax_row == 0:
                ax.set_title(f'{dataset_for_objects}')

            if ax_col == 0:
                ax.set_ylabel(f'{Label.get_symbol(plotted_param)}')

            y = list(map(lambda yi: yi[f'{plotted_param}'], data_for_obj))

            x = list(map(lambda xi: math.sqrt(math.pow(xi["x"], 2) + math.pow(xi["z"], 2)), data_for_obj))

            ax.scatter(x, y, label=f'{obj}', color=objects[obj]['color'], marker=objects[obj]['marker'])
            ax.legend()

        ax_row += 1

    ax_col += 1

plt.show()

import numpy as np
from matplotlib import pyplot as plt

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_unification.data_maps import ImageEntropyAnalysisDataMap
from data_unification.enums import PersistentNames
from data_visualisation.labels import Label
from examples.utils import ALL_OBJECTS_LIST, DATASETS_DICT

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

compared_param = PersistentNames.STANDARD_DEVIATION_OF_PROCESSED_IMAGE

datasets_for_objects = DATASETS_DICT

histogram_values_to_ignore = [0]

x = np.arange(len(ALL_OBJECTS_LIST))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0
fig, ax = plt.subplots(layout='constrained')
data_to_bar_plot = {}

for dataset in datasets_for_objects.keys():

    data_to_bar_plot[dataset] = []

    for obj in ALL_OBJECTS_LIST:
        app_manager.set_object(object=obj)
        data_for_obj = (app_manager
                        .load_data_from_db()
                        .custom_data({"dataset": dataset}))

        data_map = ImageEntropyAnalysisDataMap(data_for_obj, {},
                                               histogram_values_to_ignore=histogram_values_to_ignore)

        value_for_bar = max(list(map(lambda v: 6 * v, data_map.get_values(compared_param))))

        data_to_bar_plot[dataset].append(value_for_bar)

for dataset, value in data_to_bar_plot.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, value, width, label=dataset)
    ax.bar_label(rects, padding=3)
    multiplier += 1

ax.set_ylabel(f'6 x {Label.get_symbol(compared_param)}', fontsize=20)
ax.set_title(f'Max 6x{Label.get_symbol(compared_param)} value for each object and dataset', fontsize=20)
ax.set_xticks(x + width, ALL_OBJECTS_LIST, fontsize=20)
ax.legend(loc='upper left', ncols=3, fontsize=20)
ax.set_ylim(0, 40)

plt.show()
# multiple_plot.save_to_file(file_name=f'{path_to_save_figures}/std_dev_range/{dataset}', dpi=600)

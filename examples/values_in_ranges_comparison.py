import statistics

import numpy as np
from matplotlib import pyplot as plt

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_unification.data_maps import ImageEntropyAnalysisDataMap
from data_unification.enums import PersistentNames, KeyValues
from data_visualisation.labels import Label
from examples.utils import ALL_OBJECTS_LIST, DATASETS_DICT

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

compared_param = PersistentNames.ENTROPY_IN_BITS_OF_PROCESSED_IMAGE
values_groups = [0, 100, 200, 300, 400, 500, 600, 700, 800]

datasets_for_objects = DATASETS_DICT

histogram_values_to_ignore = [0]

fig, ax = plt.subplots(layout='constrained')


for obj in ALL_OBJECTS_LIST:
    app_manager.set_object(object=obj)

    values_for_all_datasets_dict = {}

    for dataset in datasets_for_objects.keys():
        values_for_all_datasets = []

        data_for_obj = (app_manager
                        .load_data_from_db()
                        .custom_data({"dataset": dataset}))

        data_map = ImageEntropyAnalysisDataMap(data_for_obj, {},
                                               histogram_values_to_ignore=histogram_values_to_ignore)

        values_for_all_datasets.extend(data_map.get_values(compared_param))
        values_used_to_group = data_map.get_values(KeyValues.DISTANCE)

        values_dict = dict(zip(values_used_to_group, values_for_all_datasets))

        values_for_all_datasets_dict.update(values_dict)

    for i in range(1, len(values_groups)):

        filtered_dict = {k: v for k, v in values_for_all_datasets_dict.items() if values_groups[i-1] <= k <= values_groups[i]}

        filtered_values = filtered_dict.values()

        mean_val = statistics.mean(filtered_values)
        std_dev = statistics.stdev(filtered_values)







ax.set_ylabel(f'6 x {Label.get_symbol(compared_param)}', fontsize=20)
ax.set_title(f'Max 6x{Label.get_symbol(compared_param)} value for each object and dataset', fontsize=20)
ax.set_xticks(x + width, ALL_OBJECTS_LIST, fontsize=20)
ax.legend(loc='upper left', ncols=3, fontsize=20)
ax.set_ylim(0, 40)

plt.show()
# multiple_plot.save_to_file(file_name=f'{path_to_save_figures}/std_dev_range/{dataset}', dpi=600)

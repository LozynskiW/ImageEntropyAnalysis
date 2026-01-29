from matplotlib import pyplot as plt

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_unification.data_maps import ImageEntropyAnalysisDataMap
from data_unification.enums import PersistentNames, TransientValues
from examples.utils import ALTERNATING_BACKGROUND_LIGHT_DATASETS_DICT

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

datasets_for_objects = ALTERNATING_BACKGROUND_LIGHT_DATASETS_DICT

objects_list = ['sphere']

for obj in objects_list:
    app_manager.set_object(object=obj)

    for dataset in datasets_for_objects.keys():
        fig, ax = plt.subplots()
        data_for_obj = (app_manager
                        .load_data_from_db()
                        .custom_data({"dataset": dataset}))

        data_map = ImageEntropyAnalysisDataMap(data_for_obj, {}, histogram_values_to_ignore=[])

        histogram_values = data_map.get_values(TransientValues.HISTOGRAM_VALUES)[0]
        histogram_values_counts = data_map.get_values(PersistentNames.HISTOGRAM_OF_PROCESSED_IMAGE)[0]

        ax.bar(histogram_values, histogram_values_counts)
        ax.set_ylabel('Counts')
        ax.set_title(f'{dataset}')
        plt.show()

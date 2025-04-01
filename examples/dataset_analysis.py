from application_management.app import AppManager
from image_processing.ready_to_use_systems import information_entropy_based_system as information_entropy_sys
from consts.datasets_for_object import DEER
from consts.system_util import PATH_TO_MAIN_FOLDER

object_to_analyze = DEER.dataset_name()
datasets_to_analyze = DEER.all_datasets()

used_system = information_entropy_sys.information_entropy_based_system
used_system.global_verbose_mode = True

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)
app_manager.set_image_processing_system(used_system)

app_manager.set_object(object=object_to_analyze)

app_manager.analyze_dataset(save_to_db=True, verbose_mode=True, show_images=False, memory=True)

# for i in range(0, len(list(datasets_to_analyze))):
#
#     data_from_db = app_manager.local_storage.set_object().load_data().specific_dataset_for_one_object(
#             dataset=list(datasets_to_analyze)[i],
#     )
#
#     analysis_method_test = overall_data_analysis(data=data_from_db, data_name=str(list(datasets_to_analyze)[i]))
#     analysis_method_test.general_description()


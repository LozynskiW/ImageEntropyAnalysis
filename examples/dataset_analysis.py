from application_management.app import AppManager
from image_data_logs_readers.gps_logs import JsonLogsReader
from image_processing.ready_to_use_systems import luminance_threshold_based_system as luminance_entropy_sys
from consts.datasets_for_object import DEER
from consts.system_util import PATH_TO_MAIN_FOLDER

object_to_analyze = "sphere"
datasets_to_analyze = DEER.all_datasets()

used_system = luminance_entropy_sys.luminance_threshold_image_segmentation_theoretical_data
used_system.global_verbose_mode = True

app_manager = AppManager()
app_manager.set_main_folder(f"{PATH_TO_MAIN_FOLDER}/manual")
app_manager.set_image_processing_system(used_system)
app_manager.set_object(object=object_to_analyze)

gps_logs_reader = JsonLogsReader("D:/python/ImageEntropyAnalysis/blender3d_intergration/trajectories_api/calculated_trajectories/manual/manual_gps.json")

app_manager.analyze_dataset_only_segmentation(save_to_db=True, update=True, verbose_mode=True, show_images=False, log_reader=gps_logs_reader)

# for i in range(0, len(list(datasets_to_analyze))):
#
#     data_from_db = app_manager.local_storage.set_object().load_data().specific_dataset_for_one_object(
#             dataset=list(datasets_to_analyze)[i],
#     )
#
#     analysis_method_test = overall_data_analysis(data=data_from_db, data_name=str(list(datasets_to_analyze)[i]))
#     analysis_method_test.general_description()


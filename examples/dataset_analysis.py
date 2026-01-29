from application_management.app import AppManager
from image_data_logs_readers.gps_logs import JsonLogsReader
from image_processing.ready_to_use_systems import luminance_threshold_based_system as luminance_entropy_sys
from consts.system_util import PATH_TO_MAIN_FOLDER

objects_to_analyze = ["sphere"]
datasets_to_analyze = ["white_noise_background_636363FF", "white_noise_background_A5A5A5FF", "white_noise_background_CFCFCFFF", "white_noise_background_F0F0F0FF"]

used_system = luminance_entropy_sys.luminance_threshold_image_segmentation_theoretical_data
used_system.global_verbose_mode = True

app_manager = AppManager()
app_manager.set_main_folder(f"{PATH_TO_MAIN_FOLDER}/manual")
app_manager.set_image_processing_system(used_system)

for object_to_analyze in objects_to_analyze:
    app_manager.set_object(object=object_to_analyze)

    gps_logs_reader = JsonLogsReader("D:/python/ImageEntropyAnalysis/blender3d_intergration/trajectories_api/calculated_trajectories/manual/manual_gps.json")

    app_manager.analyze_dataset_only_segmentation(
        save_to_db=True,
        update=True,
        verbose_mode=True,
        show_images=False,
        log_reader=gps_logs_reader,
        datasets=datasets_to_analyze)

from application_management.app import app_manager
from image_processing.ready_to_use_systems import luminance_threshold_based_system as threshold_sys
from consts.datasets_for_object import DEER as all_datasets_for_deer
from consts.data_to_plot import ENTROPY_OF_PROCESSED_IMAGE

used_system = threshold_sys.luminance_threshold_based_system

app_manager = app_manager()
app_manager.set_main_folder('D:/artykuly/wat_2/test_animations')
app_manager.set_image_processing_system(used_system)

app_manager.set_object(object='deer')

used_system.global_verbose_mode = True

data_from_db = app_manager.load_data_from_db().multiple_datasets(
        datasets=all_datasets_for_deer['h20m_set'],
        is_valid=True,
        was_processed=True,
        is_target_detected=True
)

app_manager.set_data_from_db(data_from_db=data_from_db)

app_manager.plot_data_from_db(data_to_y_axis=ENTROPY_OF_PROCESSED_IMAGE, data_to_x_axis="file_name").scatter_plot()
# app_manager.plot_data_from_db().line_plot()

# app_manager.analyze_dataset(save_to_db=True, verbose_mode=True, show_images=False, memory=False)

""" data inspection
for i in range(0, len(list(all_datasets_for_deer.values()))):

    data_from_db = test.load_data().specific_dataset_for_one_object(
            dataset=list(all_datasets_for_deer.values())[i],
    )

    analysis_method_test = overall_data_analysis(data=data_from_db, data_name=str(list(all_datasets_for_deer.values())[i]))
    analysis_method_test.general_description()
"""
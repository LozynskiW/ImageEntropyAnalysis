from application_management.app import AppManager
from image_processing.ready_to_use_systems import luminance_threshold_based_system as threshold_sys
from consts.datasets_for_object import DEER
from consts.data_to_plot import X_axis, Y_axis
from data_visualisation.consts.plot_options import PlotOptionsBuilder

used_system = threshold_sys.luminance_threshold_based_system

app_manager = AppManager()
app_manager.set_main_folder('D:/artykuly/wat_2/test_animations')
app_manager.set_image_processing_system(used_system)

app_manager.set_object(object='deer')

used_system.global_verbose_mode = True

data_from_db = app_manager.load_data_from_db().multiple_datasets(
    datasets=DEER.all_datasets(),
    is_valid=True,
    was_processed=True,
    is_target_detected=True
)

data_from_db_filtered = list(filter(lambda x: x['dataset'] == "h20m_r100m", data_from_db))

app_manager.set_data_from_db(data_from_db=data_from_db)

builder = PlotOptionsBuilder()
plot_options = builder \
    .x_axis(X_axis.YAW_ANGLE_IN_DEG) \
    .y_axis(Y_axis.ENTROPY_OF_PROCESSED_IMAGE) \
    .color('r') \
    .build()

# app_manager.plot_2d(plot_options=plot_options).scatter_plot()

plot_options_3d = builder \
    .x_axis(X_axis.HEIGHT) \
    .y_axis(X_axis.PITCH_ANGLE_IN_DEG) \
    .z_axis(Y_axis.ENTROPY_OF_PROCESSED_IMAGE) \
    .build()

# app_manager.plot_3d(plot_options=plot_options).surface_plot()
app_manager.heatmap(plot_options_3d).reduce_to_means()
# Analiza zdjęć i dopisywanie danych do bazy
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

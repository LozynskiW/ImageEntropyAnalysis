from application_management.app import AppManager
from consts.datasets_for_object import DEER
from consts.data_to_plot import X_axis, Y_axis
from data_visualisation.consts.plot_options import PlotOptionsBuilder
from consts.system_util import PATH_TO_MAIN_FOLDER

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)
app_manager.set_object(object=DEER.dataset_name())

data_from_db = app_manager.load_data_from_db().multiple_datasets(
    datasets=DEER.all_datasets(),
    is_valid=True,
    was_processed=True,
    is_target_detected=True
)

app_manager.set_data_from_db(data_from_db=data_from_db)

builder = PlotOptionsBuilder()

plot_options_3d = builder \
    .x_axis(X_axis.PITCH_ANGLE_IN_DEG) \
    .y_axis(X_axis.HEIGHT) \
    .z_axis(Y_axis.ENTROPY_OF_PROCESSED_IMAGE) \
    .build()

app_manager.heatmap(plot_options_3d).reduce_to_means()

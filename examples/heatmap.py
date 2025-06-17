from application_management.app import AppManager
from consts.datasets_for_object import DEER
from consts.data_to_plot import X_axis, Y_axis
from data_visualisation.consts.plot_options import PlotOptionsBuilder
from consts.system_util import PATH_TO_MAIN_FOLDER
import statistics

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)
app_manager.set_object(object='sphere')

data_from_db = (app_manager
                .load_data_from_db()
                .custom_data({}))

app_manager.set_data_from_db(data_from_db=data_from_db)

builder = PlotOptionsBuilder()

plot_options_3d = builder \
    .x_axis("x") \
    .y_axis("z") \
    .z_axis("standard_deviation_of_processed_image") \
    .build()


def mapping_fun(data):
    if data is None:
        return 0
    return statistics.stdev(data[2:])


app_manager.heatmap(plot_options_3d).plot_single_dataset_map_results_by_fun()

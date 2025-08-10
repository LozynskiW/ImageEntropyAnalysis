import statistics

from application_management.app import AppManager
from data_visualisation.models import FigureOptions
from consts.system_util import PATH_TO_MAIN_FOLDER
from data_visualisation.plotting_facade import PlottingFacade

object_to_plot = 'cube'
dataset_to_plot = 'white_only'

plotted_param = 'standard_deviation_of_processed_image'
x_axis = "x"
y_axis = "z"

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)
app_manager.set_object(object='sphere')

data_from_db = (app_manager
                .load_data_from_db()
                .custom_data({}))

app_manager.set_data_from_db(data_from_db=data_from_db)

figure_options = FigureOptions(
    x_axis_label=x_axis,
    y_axis_label=y_axis,
    z_axis_label=plotted_param
)


def mapping_fun(data):
    if data is None:
        return 0
    return statistics.stdev(data[2:])


PlottingFacade.heatmap().plot_data(data_from_db=data_from_db, figure_options=figure_options)

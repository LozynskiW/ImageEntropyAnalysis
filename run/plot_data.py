import math

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER
from data_visualisation.models import FigureOptions, PlotOptions
from data_visualisation.plotting_facade import PlottingFacade

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)
app_manager.set_object(object='sphere')

data_from_db = (app_manager
                .load_data_from_db()
                .custom_data({}))

y = list(map(lambda yi: sum(yi["histogram_of_processed_image"][180:]) / sum(yi["histogram_of_processed_image"][:180]), data_from_db))

x = list(map(lambda xi: math.sqrt(math.pow(xi["x"],2) + math.pow(xi["z"],2)), data_from_db))

figure_options = FigureOptions(
    x_axis_label="distance from object",
    y_axis_label="number of pixels above 180"
)

plot_options = PlotOptions(x=x, y=y)
PlottingFacade.manual_plot().scatter_plot(plot_options, figure_options)
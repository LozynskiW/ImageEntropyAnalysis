import math

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER
from data_visualisation.models import PlotOptions, FigureOptions, PlotColor
from data_visualisation.plotting_facade import PlottingFacade

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

objects = {
    'cube': PlotColor.BLUE,
    'cone': PlotColor.GREEN,
    'sphere': PlotColor.MAGENTA,
    'cylinder': PlotColor.YELLOW
}

plotted_param = "standard_deviation_of_processed_image"

figure_options = FigureOptions(
    x_axis_label="distance from object",
    y_axis_label=f'{plotted_param}'
)

multiple_plot = PlottingFacade.multiple_plot().scatter_plot(figure_options)

for obj in objects.keys():
    app_manager.set_object(object=obj)
    data_for_obj = (app_manager
                     .load_data_from_db()
                     .custom_data({"dataset": "manual"}))

    # y = list(map(lambda yi: sum(yi["histogram_of_processed_image"][1:]) / sum(yi["histogram_of_processed_image"]), data_for_obj))

    y = list(map(lambda yi: yi[f'{plotted_param}'], data_for_obj))

    x = list(map(lambda xi: math.sqrt(math.pow(xi["x"], 2) + math.pow(xi["z"], 2)), data_for_obj))

    plot_options = PlotOptions(x=x, y=y, color=objects[obj], label=obj)
    multiple_plot.add_data(plot_options)

multiple_plot.show()

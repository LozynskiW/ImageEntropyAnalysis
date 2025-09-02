from application_management.app import AppManager
from data_visualisation._implementations.heatmap import HeatmapConfig
from data_visualisation.models import FigureOptions
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_visualisation.plotting_facade import PlottingFacade

object_to_plot = 'cone'
dataset_for_objects = 'manual'  # manual white_noise white_only
path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

plotted_param = 'number of target pixels'
values_mapping_fun = lambda xi: sum(xi["histogram_of_processed_image"][1:])

x_axis = "x"
y_axis = "z"

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)
app_manager.set_object(object=object_to_plot)

data_from_db = (app_manager
                .load_data_from_db()
                .custom_data({"dataset": {"$in": datasets_for_objects}}))

app_manager.set_data_from_db(data_from_db=data_from_db)

figure_options = FigureOptions(
    x_axis_label=x_axis,
    y_axis_label=y_axis,
    z_axis_label=plotted_param,
    title=f'{object_to_plot}: {plotted_param}'
)

heatmap_config = HeatmapConfig(
    show_cbar=False,
    show_annotations=True,
    to_percentage=False,
    values_mapping_fun=values_mapping_fun
)

PlottingFacade.heatmap().plot_data(
    data_from_db=data_from_db,
    figure_options=figure_options,
    config=heatmap_config
)

# PlottingFacade.heatmap().save_to_file(
#     data_from_db=data_from_db,
#     figure_options=figure_options,
#     config=heatmap_config,
#     file_name=f'{path_to_save_figures}/{object_to_plot}_heatmap_{plotted_param}'
# )

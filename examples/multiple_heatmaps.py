from application_management.app import AppManager
from data_visualisation._implementations.heatmap import HeatmapConfig
from data_visualisation.models import FigureOptions
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_visualisation.plotting_facade import PlottingFacade

objects_to_plot = ['cube', 'cone', 'sphere', 'cylinder']
datasets_for_objects = ['manual', 'white_noise', 'white_only']
path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

plotted_param = 'entropy_in_bits_of_processed_image'
x_axis = "x"
y_axis = "z"

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

for obj_to_plot in objects_to_plot:
    app_manager.set_object(object=obj_to_plot)

    for dataset in datasets_for_objects:

        data_from_db = (app_manager
                        .load_data_from_db()
                        .custom_data({"dataset": f'{dataset}'}))

        app_manager.set_data_from_db(data_from_db=data_from_db)

        figure_options = FigureOptions(
            x_axis_label=x_axis,
            y_axis_label=y_axis,
            z_axis_label=plotted_param,
            title=f'{obj_to_plot} - {dataset} - {plotted_param}'
        )

        heatmap_config = HeatmapConfig(
            show_cbar=False,
            show_annotations=True
        )

        PlottingFacade.heatmap().save_to_file(
            data_from_db=data_from_db,
            figure_options=figure_options,
            config=heatmap_config,
            file_name=f'{path_to_save_figures}/{obj_to_plot}_heatmap_{dataset}_{plotted_param}'
        )

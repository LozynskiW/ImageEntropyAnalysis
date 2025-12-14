from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_visualisation.models import PlotOptions, FigureOptions, PlotColor
from data_visualisation.plotting_facade import PlottingFacade

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

objects = [
    'sphere', 'cube', 'cone', 'cylinder'
]

datasets_for_objects = {
    'white_only': PlotColor.RED,
    'gradient': PlotColor.GREEN,
    'white_noise': PlotColor.BLUE
}

plotted_params_pairs = [
    ("standard_deviation_of_processed_image", "expected_value_of_original_image"),
    ("entropy_in_bits_of_processed_image", "expected_value_of_original_image")
]

for params_pair in plotted_params_pairs:

    figure_options = FigureOptions(
        x_axis_label=params_pair[0],
        y_axis_label=params_pair[1]
    )

    multiple_plot = PlottingFacade.multiple_plot()
    multiple_plot.configure(figure_options)

    for obj in objects:
        app_manager.set_object(object=obj)

        for dataset in datasets_for_objects.keys():
            data_for_obj = (app_manager
                            .load_data_from_db()
                            .custom_data({"dataset": dataset}))

            param_to_x = list(map(lambda yi: yi[params_pair[0]], data_for_obj))
            param_to_y = list(map(lambda yi: yi[params_pair[1]], data_for_obj))

            plot_options = PlotOptions(x=param_to_x, y=param_to_y, color=datasets_for_objects[dataset], label=f'{dataset}')
            multiple_plot.add_scatter_plot(plot_options)

        # multiple_plot.save_to_file(file_name=f'{path_to_save_figures}/{obj}_{plotted_param}', dpi=200)
        multiple_plot.show()
        multiple_plot.clear()

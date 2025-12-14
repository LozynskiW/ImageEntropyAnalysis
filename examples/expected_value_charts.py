import numpy as np
from scipy.interpolate import make_smoothing_spline

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_unification.data_maps import SortableDataMap, ImageEntropyAnalysisDataMap, SmoothingDataMap
from data_unification.enums import KeyValues, PersistentNames
from data_visualisation.models import PlotOptions, FigureOptions, PlotColor, PlotOptionsWithOYErrors, PlotMarker, \
    ViridisColors
from data_visualisation.plotting_facade import PlottingFacade

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

objects = {
    'cube': PlotColor.BLUE,
    'cone': PlotColor.GREEN,
    'sphere': PlotColor.MAGENTA,
    'cylinder': PlotColor.YELLOW
}

dataset_for_objects = 'white_noise'

figure_options = FigureOptions(
    x_axis_label="distance from object",
    y_axis_label="expected_value_of_processed_image"
)

# all possible values
# z_values = [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200,
#             240, 280, 320, 360, 400, 450, 500]

z_values = [10, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 500]

multiple_plot = PlottingFacade.multiple_plot()
multiple_plot.configure(figure_options)

for obj in objects.keys():
    app_manager.set_object(object=obj)
    data_for_obj = (app_manager
                    .load_data_from_db()
                    .custom_data({"dataset": dataset_for_objects}))

    data_map = ImageEntropyAnalysisDataMap(data_for_obj, {KeyValues.DISTANCE}, histogram_values_to_ignore=[0])
    sorted_data = SortableDataMap(data_map=data_map, sorting_function=sorted)
    smoothed_vals = SmoothingDataMap(data_map=sorted_data, smoothing_window=10)

    for z in z_values:

        distance = sorted_data.get_values_for_where(
            values_key=KeyValues.DISTANCE,
            values_where_key=PersistentNames.Z, min_val=z, max_val=z)
        exp_val = sorted_data.get_values_for_where(values_key=PersistentNames.EXPECTED_VALUE_OF_PROCESSED_IMAGE,
                                                     values_where_key=PersistentNames.Z, min_val=20, max_val=20)
        std_devs = sorted_data.get_values_for_where(values_key=PersistentNames.STANDARD_DEVIATION_OF_PROCESSED_IMAGE,
                                                      values_where_key=PersistentNames.Z, min_val=20, max_val=20)

        color = ViridisColors.next_color()
        color_light = ViridisColors.get_lighter_version()

        plot_options = PlotOptions(
            x=distance,
            y=exp_val,
            color=color,
            label=f"Height={z}[m]",
            marker=PlotMarker.X
        )
        multiple_plot.add_scatter_plot(plot_options)

        spl = make_smoothing_spline(distance, exp_val)
        grid = np.linspace(distance[0], distance[-1], len(distance))

        spl_plot_options = PlotOptions(
            x=grid,
            y=spl(grid),
            color=color,
            label=f"spline for H={z}[m]"
        )
        spl_plot_options_with_errors = PlotOptionsWithOYErrors(
            plot_options=spl_plot_options,
            y_errors=std_devs,
            x_errors=[],
            errors_color=color_light
        )
        multiple_plot.add_line_with_errors_plot(spl_plot_options_with_errors)

    multiple_plot.show()
    # multiple_plot.save_to_file(
    #     file_name=f'{path_to_save_figures}/all_objs_{dataset_for_objects}_{plotted_param}',
    #     dpi=1200
    # )

    multiple_plot.clear()

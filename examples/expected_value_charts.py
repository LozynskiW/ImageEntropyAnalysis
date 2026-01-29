import numpy as np
from scipy.optimize import curve_fit

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_unification.data_maps import ImageEntropyAnalysisDataMap
from data_unification.enums import KeyValues, PersistentNames
from data_visualisation.labels import Label
from data_visualisation.models import PlotOptions, FigureOptions, PlotColor, PlotOptionsWithOYErrors, PlotMarker
from data_visualisation.plotting_facade import PlottingFacade

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

objects = ['cube', 'cone', 'sphere', 'cylinder']

datasets = {
    'white_noise': {'color': PlotColor.BLUE, 'marker': PlotMarker.X},
    'gradient': {'color': PlotColor.GREEN, 'marker': PlotMarker.PLUS},
    'white_only': {'color': PlotColor.RED, 'marker': PlotMarker.POINT}
}

figure_options = FigureOptions(
    x_axis_label=f'{Label.get_symbol(KeyValues.DISTANCE)}',
    y_axis_label=f'{Label.get_symbol(PersistentNames.EXPECTED_VALUE_OF_PROCESSED_IMAGE)}',
    figure_size=(10,6)
)

z_values = [10, 60, 80, 120, 160, 200, 240, 280, 320, 360, 400, 500]


def estimating_func(x, a, b, c, d, e, f, g):
    return a * pow(x, 6) + b * pow(x, 5) + c * pow(x, 4) + d * pow(x, 3) + e * pow(x, 2) + f * pow(x, 1) + g * pow(x, 0)


multiple_plot = PlottingFacade.multiple_plot()

for obj in objects:

    for dataset in datasets.keys():
        app_manager.set_object(object=obj)
        data_for_obj = (app_manager
                        .load_data_from_db()
                        .custom_data({"dataset": dataset}))

        figure_options.title = obj
        multiple_plot.configure(figure_options)

        data_map = ImageEntropyAnalysisDataMap(data_for_obj, {}, histogram_values_to_ignore=[0])

        num_of_pixels = list(map(lambda n : int(sum(n)), data_map.get_values(PersistentNames.HISTOGRAM_OF_PROCESSED_IMAGE)))
        distance = data_map.get_values(KeyValues.DISTANCE)
        exp_val = data_map.get_values(PersistentNames.EXPECTED_VALUE_OF_PROCESSED_IMAGE)
        std_devs = data_map.get_values(PersistentNames.STANDARD_DEVIATION_OF_PROCESSED_IMAGE)

        plot_options = PlotOptions(
            x=distance,
            y=exp_val,
            label=f"{dataset}",
            marker=datasets[dataset]['marker'],
            color=datasets[dataset]['color'],
            marker_size=10,
        )
        multiple_plot.add_scatter_plot(plot_options)

        params = curve_fit(f=estimating_func, xdata=distance, ydata=exp_val)
        optimal_params = params[0]
        print(f'{obj}-{dataset}-params: {optimal_params}')

        x_fit = np.linspace(min(distance), max(distance), len(std_devs))
        y_fit = estimating_func(x_fit, optimal_params[0], optimal_params[1], optimal_params[2], optimal_params[3],
                               optimal_params[4], optimal_params[5], optimal_params[6])

        spl_plot_options = PlotOptions(
            x=x_fit,
            y=y_fit,
            color=datasets[dataset]['color'],
            label=f""
        )
        spl_plot_options_with_errors = PlotOptionsWithOYErrors(
            plot_options=spl_plot_options,
            y_errors=std_devs,
            x_errors=[],
            errors_color=datasets[dataset]['color']
        )
        multiple_plot.add_line_with_errors_plot(spl_plot_options_with_errors)

    # multiple_plot.show()
    multiple_plot.save_to_file(
        file_name=f'{path_to_save_figures}/{obj}_all_datasets_exp_val_comparison',
        dpi=1200
    )

    multiple_plot.clear()

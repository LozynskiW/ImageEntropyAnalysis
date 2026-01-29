import numpy as np

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_unification.data_maps import ImageEntropyAnalysisDataMap
from data_unification.enums import KeyValues
from data_visualisation.labels import Label
from data_visualisation.models import PlotOptions, FigureOptions, PlotColor, PlotMarker, PlotFontSize
from data_visualisation.plotting_facade import PlottingFacade

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

objects = [
    'sphere', 'cube', 'cone', 'cylinder'
]

datasets_for_objects = {
    'white_only': {'color': PlotColor.RED, 'marker': PlotMarker.POINT},
    'gradient': {'color': PlotColor.GREEN, 'marker': PlotMarker.STAR},
    'white_noise': {'color': PlotColor.BLUE, 'marker': PlotMarker.PLUS}
}

grayscale_histogram_values = np.linspace(1, 255, num=254)

plotted_params = {
    "Log10(No)": lambda x: np.log10(sum(x["histogram_of_processed_image"][1:]))
}

multiple_plot = PlottingFacade.multiple_plot()

for plotted_param in plotted_params:

    figure_options = FigureOptions(
        x_axis_label=f'{Label.get_symbol(KeyValues.DISTANCE)}',
        y_axis_label=f'{Label.get_symbol(plotted_param)}',
        font_size=PlotFontSize.BIG
    )

    for obj in objects:
        app_manager.set_object(object=obj)
        figure_options.title = obj

        multiple_plot.configure(figure_options)

        for dataset in datasets_for_objects.keys():
            data_for_obj = (app_manager
                            .load_data_from_db()
                            .custom_data({"dataset": dataset}))

            data_map = ImageEntropyAnalysisDataMap(data_for_obj, {}, histogram_values_to_ignore=[0])

            plotted_param_y = list(map(plotted_params[plotted_param], data_for_obj))

            distance = data_map.get_values(KeyValues.DISTANCE)

            plot_options = PlotOptions(x=distance, y=plotted_param_y,
                                       color=datasets_for_objects[dataset]['color'],
                                       label=f'{dataset}',
                                       marker=datasets_for_objects[dataset]['marker'])
            multiple_plot.add_scatter_plot(plot_options)

        multiple_plot.save_to_file(file_name=f'{path_to_save_figures}/{obj}_{plotted_param}', dpi=800)
        # multiple_plot.show()
        multiple_plot.clear()

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_unification.data_maps import ImageEntropyAnalysisDataMap
from data_unification.enums import PersistentNames, KeyValues
from data_visualisation.labels import Label
from data_visualisation.models import PlotOptions, FigureOptions
from data_visualisation.plotting_facade import PlottingFacade
from examples.utils import ALL_OBJECTS_LIST, DATASETS_DICT, objects

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

plotted_params_pairs = [
    (KeyValues.DISTANCE, PersistentNames.STANDARD_DEVIATION_OF_PROCESSED_IMAGE)
]

datasets_for_objects = DATASETS_DICT

histogram_values_to_ignore = [0]

for params_pair in plotted_params_pairs:

    for dataset in datasets_for_objects.keys():

        multiple_plot = PlottingFacade.multiple_plot()
        figure_options = FigureOptions(
            x_axis_label=f'{Label.get_symbol(params_pair[0])}',
            y_axis_label=f'6 x {Label.get_symbol(params_pair[1])}',
            title=f'{dataset}'
        )

        multiple_plot.configure(figure_options)

        for obj in ALL_OBJECTS_LIST:
            app_manager.set_object(object=obj)
            data_for_obj = (app_manager
                            .load_data_from_db()
                            .custom_data({"dataset": dataset}))

            data_map = ImageEntropyAnalysisDataMap(data_for_obj, {},
                                                   histogram_values_to_ignore=histogram_values_to_ignore)

            param_to_x = data_map.get_values(params_pair[0])
            param_to_y = list(map(lambda x: 6 * x, data_map.get_values(params_pair[1])))

            plot_options = PlotOptions(x=param_to_x, y=param_to_y,
                                       color=objects[obj]['color'],
                                       marker=objects[obj]['marker'],
                                       label=f'{obj}',
                                       title=f'{dataset}')

            multiple_plot.add_scatter_plot(plot_options)

        multiple_plot.save_to_file(file_name=f'{path_to_save_figures}/std_dev_range/{dataset}', dpi=600)
        # multiple_plot.show()
        multiple_plot.clear()

from app.application_management.app import app_manager

from data.datasets_for_object import deer as all_datasets_for_deer

from analysis_outcome.data_format_unification import to_dict

from app.data_visualisation.analysis_outcome.basic_plot_functions import scatter_plot
from app.data_visualisation.util.figure_and_plot_style import FigureBuilder

test = app_manager()

test.set_object(object='deer')

verbose_mode = False
show_images = False

data_from_db = test.load_data_from_db().multiple_datasets(
        datasets=all_datasets_for_deer['h20m_set'],
        is_valid=True,
        was_processed=True,
        is_target_detected=True
)

test.set_data_from_db(data_from_db=data_from_db)

data_to_plot = to_dict.unify_for_one_class_of_object(data_from_db=test.get_data_from_db(),
                                                     data_to_x_axis='file_name',
                                                     data_to_y_axis='fill_factor')

figure_builder = FigureBuilder()
figure_builder.build()

scatter_plot(data_to_plot=data_to_plot, figure_builder=figure_builder, style=None)

print("TESTGROUND")
print(data_to_plot.keys())
print(data_to_plot[list(data_to_plot.keys())[0]].keys())
print(data_to_plot[list(data_to_plot.keys())[0]]['ox'])
print(data_to_plot[list(data_to_plot.keys())[0]]['oy'])
import math

import numpy as np
from matplotlib import pyplot as plt

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER
from data_analysis.statistical_calculations_utils import ExpectedValueFromValuesCounts, VarianceFromValuesCounts
from data_visualisation.models import PlotOptions, FigureOptions
from data_visualisation.plotting_facade import ManualPlot, PlottingFacade

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)
app_manager.set_object(object='cube')

data_from_db = (app_manager
                .load_data_from_db()
                .custom_data({ "dataset": "manual" }))

data_from_db_without_zeros = data_from_db[1:]

expected_values_list = list(map(lambda yi: ExpectedValueFromValuesCounts(
        variable_values_counts=yi["histogram_of_processed_image"][1:]).value, data_from_db_without_zeros))

variance_list = list(map(lambda yi: VarianceFromValuesCounts(
        variable_values_counts=yi["histogram_of_processed_image"][1:]).value, data_from_db_without_zeros))

y = list(map(lambda yi: sum(yi["histogram_of_processed_image"][180:]) / sum(yi["histogram_of_processed_image"][:180]), data_from_db))

x = list(map(lambda xi: math.sqrt(math.pow(xi["x"],2) + math.pow(xi["z"],2)), data_from_db))

figure_options = FigureOptions(
    x_axis_label="distance from object",
    y_axis_label="number of pixels above 180"
)

plot_options = PlotOptions(x=x, y=y)
PlottingFacade.manual_plot().scatter_plot(plot_options, figure_options)

y = list(map(lambda yi: sum(yi["histogram_of_processed_image"][2:]), data_from_db))

x = list(map(lambda xi: math.sqrt(math.pow(xi["x"],2) + math.pow(xi["z"],2)), data_from_db))

figure_options = FigureOptions(
    x_axis_label="distance from object",
    y_axis_label="number of pixels"
)

plot_options = PlotOptions(x=x, y=y)
PlottingFacade.manual_plot().scatter_plot(plot_options, figure_options)

y = list(map(lambda yi: yi["standard_deviation_of_processed_image"], data_from_db))

x = list(map(lambda xi: math.sqrt(math.pow(xi["x"],2) + math.pow(xi["z"],2)), data_from_db))

figure_options = FigureOptions(
    x_axis_label="distance from object",
    y_axis_label="standard_deviation_of_processed_image"
)

plot_options = PlotOptions(x=x, y=y)
PlottingFacade.manual_plot().scatter_plot(plot_options, figure_options)

y = list(map(lambda yi: yi["variance_of_processed_image"], data_from_db))

x = list(map(lambda xi: math.sqrt(math.pow(xi["x"],2) + math.pow(xi["z"],2)), data_from_db))

figure_options = FigureOptions(
    x_axis_label="distance from object",
    y_axis_label="variance_of_processed_image"
)

plot_options = PlotOptions(x=x, y=y)
PlottingFacade.manual_plot().scatter_plot(plot_options, figure_options)

y = list(map(lambda yi: yi["entropy_in_bits_of_processed_image"], data_from_db))

x = list(map(lambda xi: math.sqrt(math.pow(xi["x"],2) + math.pow(xi["z"],2)), data_from_db))

figure_options = FigureOptions(
    x_axis_label="distance from object",
    y_axis_label="entropy_in_bits_of_processed_image"
)

plot_options = PlotOptions(x=x, y=y)
PlottingFacade.manual_plot().scatter_plot(plot_options, figure_options)

# histograms
title = "entropia informacji dla odległości do celu równej: "
prop = "entropy_for_x_of_processed_image"
offset = 1
x = np.arange(start=offset, stop=256, step=1)
y1 = list(data_from_db[0][prop])[offset:]
y2 = list(data_from_db[len(data_from_db)-1][prop])[offset:]

fig, axs = plt.subplots(2, 1, layout='constrained')
axs[0].bar(x, y1)
axs[0].set_ylabel(f'{title} 14m')
axs[0].grid(True)

axs[1].bar(x, y2)
axs[1].set_ylabel(f'{title} 140m')
axs[1].set_xlabel('Wartosć luminancji')
axs[1].grid(True)

plt.show()

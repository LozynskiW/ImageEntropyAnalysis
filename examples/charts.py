import math
from array import array

import numpy as np

from application_management.app import AppManager
from consts.system_util import PATH_TO_MAIN_FOLDER
from data_analysis.statistical_calculations_utils import ExpectedValueFromHistogram, VarianceFromHistogram, \
    ExpectedValueFromValuesCounts, VarianceFromValuesCounts
from data_visualisation.plotting_facade import ManualPlot
from image_processing.processing_results.statistical_results import Histogram

app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)
app_manager.set_object(object='sphere')

data_from_db = (app_manager
                .load_data_from_db()
                .custom_data({}))

data_from_db_without_zeros = data_from_db[1:]

expected_values_list = list(map(lambda yi: ExpectedValueFromValuesCounts(
        variable_values_counts=yi["histogram_of_processed_image"][1:]).value, data_from_db_without_zeros))

variance_list = list(map(lambda yi: VarianceFromValuesCounts(
        variable_values_counts=yi["histogram_of_processed_image"][1:]).value, data_from_db_without_zeros))

y = list(map(lambda yi: sum(yi["histogram_of_processed_image"][180:]) / sum(yi["histogram_of_processed_image"][:180]), data_from_db))

x = list(map(lambda xi: math.sqrt(math.pow(xi["x"],2) + math.pow(xi["z"],2)), data_from_db))

ManualPlot.scatter_plot(
    x=x,
    y=y,
    x_label="distance from object",
    y_label="number of pixels above 180",
    title="number of pixels above 180 to those lower"
)


y = list(map(lambda yi: sum(yi["histogram_of_processed_image"][2:]), data_from_db))

x = list(map(lambda xi: math.sqrt(math.pow(xi["x"],2) + math.pow(xi["z"],2)), data_from_db))

ManualPlot.scatter_plot(
    x=x,
    y=y,
    x_label="distance from object",
    y_label="number of pixels",
    title=""
)

y = list(map(lambda yi: yi["standard_deviation_of_processed_image"], data_from_db))

x = list(map(lambda xi: math.sqrt(math.pow(xi["x"],2) + math.pow(xi["z"],2)), data_from_db))

ManualPlot.scatter_plot(
    x=x,
    y=y,
    x_label="distance from object",
    y_label="standard_deviation_of_processed_image",
    title=""
)

y = list(map(lambda yi: yi["variance_of_processed_image"], data_from_db))

x = list(map(lambda xi: math.sqrt(math.pow(xi["x"],2) + math.pow(xi["z"],2)), data_from_db))

ManualPlot.scatter_plot(
    x=x,
    y=y,
    x_label="distance from object",
    y_label="variance_of_processed_image",
    title=""
)

y = list(map(lambda yi: yi["entropy_in_bits_of_processed_image"], data_from_db))

x = list(map(lambda xi: math.sqrt(math.pow(xi["x"],2) + math.pow(xi["z"],2)), data_from_db))

ManualPlot.scatter_plot(
    x=x,
    y=y,
    x_label="distance from object",
    y_label="entropy_in_bits_of_processed_image",
    title=""
)
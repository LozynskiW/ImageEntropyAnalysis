from data_visualisation.analysis_outcome.data_format_unification import data_from_db_to_dict as to_dict
import data_visualisation.analysis_outcome.basic_plot_functions as bpf


class basic_plotting_functions:

    def __init__(self, data_from_db, data_to_x_axis, data_to_y_axis):
        self.__data_to_plot = to_dict.unify_for_one_class_of_object(
            data_from_db=data_from_db,
            data_to_x_axis=data_to_x_axis,
            data_to_y_axis=data_to_y_axis)

    def scatter_plot(self):

        bpf.scatter_plot(data_to_plot=self.__data_to_plot)

    def line_plot(self):

        bpf.line_plot(data_to_plot=self.__data_to_plot)

    def bar_plot(self):

        bpf.bar_plot(data_to_plot=self.__data_to_plot)

    def save_figures_for_whole_dataset(self, object):

        data_to_plot = ["pitch", "roll", "yaw", "distance_to_object", "barometric_height",
                        "horizontal_angle_of_view",
                        "vertical_angle_of_view", "mean", "entropy_of_image"]

        for data in data_to_plot:
            self.__plotting_processor.plot_whole_dataset(data=self.__data_to_plot,
                                                         ox=data,
                                                         oy="entropy_of_segmented_image",
                                                         mode="save",
                                                         filename=object)


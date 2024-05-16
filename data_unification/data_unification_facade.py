from data_visualisation.consts.plot_options import PlotOptions
from data_visualisation.analysis_outcome._data_for_visualisation import SingleDataset, SingleDataset3D, \
    MultipleDatasets, MultipleDatasetsValuesMap
from data_unification._utils import build_single_dataset, build_single_dataset_3d, build_multiple_datasets, build_multiple_datasets_value_map


class DataUnificationForPlotting:

    @staticmethod
    def unify_for_one_class_of_object(data_from_db, plot_options: PlotOptions) -> SingleDataset:
        if data_from_db['meta']['num_of_objects'] > 1:
            raise NotImplemented("Not implemented")

        del data_from_db['meta']
        datasets_in_data_from_db = list(data_from_db.keys())

        if len(datasets_in_data_from_db) == 1:
            return build_single_dataset(
                data_from_db=data_from_db,
                data_to_x_axis=plot_options.x_axis,
                data_to_y_axis=plot_options.y_axis
            )

        return SingleDataset()

    @staticmethod
    def unify_for_one_class_of_object_3d(data_from_db, plot_options: PlotOptions) -> SingleDataset3D:
        if data_from_db['meta']['num_of_objects'] > 1:
            raise NotImplemented("Not implemented")

        del data_from_db['meta']
        datasets_in_data_from_db = list(data_from_db.keys())

        if len(datasets_in_data_from_db) == 1:
            return build_single_dataset_3d(
                data_from_db=data_from_db,
                data_to_x_axis=plot_options.x_axis,
                data_to_y_axis=plot_options.y_axis,
                data_to_z_axis=plot_options.z_axis
            )

        return SingleDataset3D()

    @staticmethod
    def unify_for_one_class_of_object_multiple_datasets(data_from_db, plot_options: PlotOptions) -> MultipleDatasets:
        if data_from_db['meta']['num_of_objects'] <= 1:
            raise NotImplemented("Not implemented")

        del data_from_db['meta']
        datasets_in_data_from_db = list(data_from_db.keys())

        if len(datasets_in_data_from_db) >= 1:
            return build_multiple_datasets(
                data_from_db=data_from_db,
                data_to_x_axis=plot_options.x_axis,
                data_to_y_axis=plot_options.y_axis,
            )

        return MultipleDatasets([])

    @staticmethod
    def unify_for_one_class_of_object_multiple_datasets_single_value_map(data_from_db, plot_options: PlotOptions) -> MultipleDatasetsValuesMap:
        """
        Used to reduce data to single statistic. For example, we have dataset for income for given number of completed
        projects nad team size for each day. We have data
        Parameters
        ----------
        data_from_db
        plot_options

        Returns
        -------

        """
        if data_from_db['meta']['num_of_objects'] <= 1:
            raise NotImplemented("Not implemented")

        del data_from_db['meta']
        datasets_in_data_from_db = list(data_from_db.keys())

        if len(datasets_in_data_from_db) >= 1:
            return build_multiple_datasets_value_map(
                data_from_db=data_from_db,
                data_to_x_axis=plot_options.x_axis,
                data_to_y_axis=plot_options.y_axis,
                data_as_map_value=plot_options.z_axis
            )

        return MultipleDatasetsValuesMap([])

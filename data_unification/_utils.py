import numpy as np

from data_visualisation.analysis_outcome._data_for_visualisation import SingleDataset, SingleDataset3D, \
    MultipleDatasets, MultipleDatasets3D, MultipleDatasetsValuesMap, Single3DPoint

def build_single_3d_point(x, y, z) -> Single3DPoint:
    return Single3DPoint(x, y, z)

def build_single_dataset(data_from_db, data_to_x_axis, data_to_y_axis) -> SingleDataset:
    return SingleDataset(
        x_axis=list(map(lambda x: x[data_to_x_axis], data_from_db)),
        y_axis=list(map(lambda y: y[data_to_y_axis], data_from_db))
    )


def build_single_dataset_3d(data_from_db, data_to_x_axis, data_to_y_axis, data_to_z_axis) -> SingleDataset3D:
    return SingleDataset3D(
        x_axis=list(map(lambda x: x[data_to_x_axis], data_from_db)),
        y_axis=list(map(lambda y: y[data_to_y_axis], data_from_db)),
        z_axis=list(map(lambda z: z[data_to_z_axis], data_from_db))
    )


def build_multiple_datasets(data_from_db, data_to_x_axis, data_to_y_axis) -> MultipleDatasets:
    datasets_names = _get_datasets_from_data(data_from_db)
    datasets = []

    for dataset in datasets_names:
        data = _get_data_for_dataset(data_from_db, dataset)
        datasets.append(build_single_dataset(data, data_to_x_axis, data_to_y_axis))

    return MultipleDatasets(datasets=datasets)


def build_multiple_datasets_value_map(data_from_db,
                                      data_to_x_axis,
                                      data_to_y_axis,
                                      data_as_map_value) -> MultipleDatasetsValuesMap:
    datasets_names = _get_datasets_from_data(data_from_db)
    datasets_reduced_to_point = []
    x_labels = []
    y_labels = []

    for dataset in datasets_names:
        data = _get_data_for_dataset(data_from_db, dataset)
        x_value = float(np.mean(list(map(lambda x: x[data_to_x_axis], data))))
        y_value = float(np.mean(list(map(lambda y: y[data_to_y_axis], data))))
        z_value = float(np.mean(list(map(lambda z: z[data_as_map_value], data))))
        data_for_dataset_reduced = build_single_3d_point(x_value, y_value, z_value)
        x_labels.append(x_value)
        y_labels.append(y_value)
        datasets_reduced_to_point.append(data_for_dataset_reduced)
    x_labels_sorted_distinct = np.sort(list(set(x_labels)))
    y_labels_sorted_distinct = np.sort(list(set(y_labels)))

    return MultipleDatasetsValuesMap(points_3d_array=datasets_reduced_to_point,
                                     x_labels=x_labels_sorted_distinct,
                                     y_labels=list(reversed(y_labels_sorted_distinct)) # needed so y axis values are sorted from lowest(bottom) to highest(top)
                                     )


def build_multiple_datasets_3d(data_from_db, data_to_x_axis, data_to_y_axis, data_to_z_axis) -> MultipleDatasets3D:
    datasets_names = _get_datasets_from_data(data_from_db)
    datasets = []

    for dataset in datasets_names:
        data = _get_data_for_dataset(data_from_db, dataset)
        datasets.append(build_single_dataset_3d(data, data_to_x_axis, data_to_y_axis, data_to_z_axis))

    return MultipleDatasets3D(datasets=datasets)


def _get_datasets_from_data(data_from_db):
    return set(obj['dataset'] for obj in data_from_db)


def _get_data_for_dataset(data_from_db, dataset):
    return list(filter(lambda x: x['dataset'] == dataset, data_from_db))

import numpy as np


class _to_dict:

    @staticmethod
    def unify_for_one_class_of_object(data_from_db, data_to_x_axis, data_to_y_axis):
        if data_from_db['meta']['num_of_objects'] > 1:
            raise NotImplemented("Not implemented")

        del data_from_db['meta']
        datasets_in_data_from_db = list(data_from_db.keys())

        if len(datasets_in_data_from_db) == 1:
            return _to_dict.__return_data_for_single_dataset(data_from_db, datasets_in_data_from_db[0], data_to_x_axis, data_to_y_axis)
        return {}

    @staticmethod
    def unify_plot_style_for_data(data_to_plot, style):

        style_index = 0

        data_to_plot_with_styles = np.copy(data_to_plot)

        for dataset in data_to_plot:
            data_to_plot_with_styles[dataset] = style[style_index]

        return data_to_plot_with_styles

    @staticmethod
    def __translate_images_names_to_deg(data):

        try:
            names = [x['file'] for x in data]
        except:
            names = data

        names_deg = []

        deg_for_fps = 360 / len(names)

        for name in names:
            name = name.split('.')[0]

            names_deg.append(int(name) * deg_for_fps)

        return names_deg

    @staticmethod
    def __translate_datasets_names_to_deg(datasets):

        names_deg = []

        for dataset in datasets:
            height = dataset.split('_')[0]
            radius = dataset.split('_')[1]

            height = height.replace('h', '')
            height = float(height.replace('m', ''))
            radius = radius.replace('r', '')
            radius = float(radius.replace('m', ''))

            names_deg.append(str(round(np.arctan(radius / height) * (180 / 3.1415))))

        return names_deg

    @staticmethod
    def __return_data_for_single_dataset(data_from_db, dataset, data_to_x_axis, data_to_y_axis):
        data_from_db = data_from_db[list(data_from_db.keys())[0]]

        return {
            "ox": list(map(lambda x: x[data_to_x_axis], data_from_db)),
            "oy": list(map(lambda y: y[data_to_y_axis], data_from_db)),
        }

    @staticmethod
    def __return_data_for_multiple_datasets(data_from_db, data_to_x_axis, data_to_y_axis):
        raise NotImplemented

data_from_db_to_dict = _to_dict()
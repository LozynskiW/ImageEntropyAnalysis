import numpy as np

from application_management.app import AppManager
from image_processing.ready_to_use_systems import luminance_threshold_based_system as threshold_sys
from consts.datasets_for_object import DEER

def _translate_image_name_to_deg(data, data_length):

    deg_for_fps = 360 / data_length

    file_name = data['file_name']

    fps = int(file_name.split('.')[0])

    return fps * deg_for_fps

def _translate_dataset_name_to_deg(data):

    dataset_name = data['dataset']

    height = dataset_name.split('_')[0]
    radius = dataset_name.split('_')[1]

    height = height.replace('h', '')
    height = float(height.replace('m', ''))
    radius = radius.replace('r', '')
    radius = float(radius.replace('m', ''))

    return round(np.arctan(radius / height) * (180 / 3.1415))

used_system = threshold_sys.luminance_threshold_based_system

app_manager = AppManager()
app_manager.set_main_folder('D:/artykuly/wat_2/test_animations')
app_manager.set_image_processing_system(used_system)

app_manager.set_object(object='deer')

used_system.global_verbose_mode = True

all_data_from_db = app_manager.load_data_from_db().multiple_datasets(
    datasets=DEER.all_datasets(),
    is_valid=True,
    was_processed=True,
    is_target_detected=True
)

for dataset in DEER.all_datasets():
    data_from_db_filtered = list(filter(lambda x: x['dataset'] == dataset, all_data_from_db))

    for single_data in data_from_db_filtered:

        query = {'object': single_data['object'], 'dataset': single_data['dataset'], 'file_name': single_data['file_name']}

        data = single_data
        # INFO: commented are already done operations
        data['yaw_angle_in_deg'] = _translate_image_name_to_deg(single_data, len(data_from_db_filtered))
        data['pitch_angle_in_deg'] = _translate_dataset_name_to_deg(single_data)
        data['image_width'] = 720
        data['image_height'] = 576
        data['information_carrying_pixels'] = data['entropy_of_processed_image'] * ( data['image_width'] * data['image_height'] )

        dataset_name = data['dataset']
        height = dataset_name.split('_')[0]
        radius = dataset_name.split('_')[1]
        height = height.replace('h', '')
        height = float(height.replace('m', ''))
        radius = radius.replace('r', '')
        radius = float(radius.replace('m', ''))

        data['height'] = height
        data['radius'] = radius

        app_manager.update_data(query=query, data=data)
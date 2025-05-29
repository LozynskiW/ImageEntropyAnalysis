from skimage import io

from image_data_logs_readers.gps_logs import JsonLogsReader
from image_processing.models.image import GrayscaleImage8bit
from image_processing.ready_to_use_systems import luminance_threshold_based_system

path_to_img = "./examples/images/0001.png"
path_to_logs = "./examples/images/gps_logs.json"

img = GrayscaleImage8bit.from_image(io.imread(path_to_img))

used_system = luminance_threshold_based_system.luminance_threshold_image_segmentation_theoretical_data
image_processing_results = used_system.process_image(img)
print(image_processing_results.to_dict())

gps_logs_reader = JsonLogsReader(path_to_logs)
log_for_file = gps_logs_reader.get_log_by_image_name("0001.png")
print(log_for_file.to_dict())
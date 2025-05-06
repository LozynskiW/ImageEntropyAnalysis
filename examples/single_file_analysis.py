from skimage import io

from image_processing.models.image import GrayscaleImage8bit
from image_processing.ready_to_use_systems import information_entropy_based_system, contour_based_system, luminance_threshold_based_system

path_to_img = "./examples/images/thermal-imaging-boar.jpg"
#path_to_img = "./examples/images/thermal-imaging-humans.jpg"
#path_to_img = "./examples/images/thermal-imaging-deers.jpg"

img = GrayscaleImage8bit.from_image(io.imread(path_to_img))

used_system = luminance_threshold_based_system.luminance_threshold_based_system_no_target_detection
# used_system = information_entropy_based_system.information_entropy_based_system
# used_system = contour_based_system.contour_based_system
image_processing_results = used_system.process_image(img)

import matplotlib.pyplot as plt
from skimage import io

from image_processing.models.image import GrayscaleImage8bit
from image_processing.processing_results.statistical_results import ImageHistogram
from image_processing.ready_to_use_systems import information_entropy_based_system, contour_based_system, luminance_threshold_based_system

path_to_img = "./examples/images/thermal-imaging-boar.jpg"
#path_to_img = "./examples/images/thermal-imaging-humans.jpg"
#path_to_img = "./examples/images/thermal-imaging-deers.jpg"

img = GrayscaleImage8bit.from_image(io.imread(path_to_img))

# img_histogram = ImageHistogram(img).normalize()
#
# plt.bar(x=img_histogram.get_variables_values(), height=img_histogram.get_values_counts())
# plt.show()

used_system = luminance_threshold_based_system.luminance_threshold_based_system_no_target_detection
# used_system = information_entropy_based_system.information_entropy_based_system
# used_system = contour_based_system.contour_based_system
test = used_system.process_image(img)

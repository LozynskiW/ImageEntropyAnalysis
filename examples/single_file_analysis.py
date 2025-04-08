from skimage import io
from image_processing.ready_to_use_systems import information_entropy_based_system, contour_based_system, luminance_threshold_based_system

path_to_img = "./images/thermal-imaging-boar.jpg"
#path_to_img = "./images/thermal-imaging-humans.jpg"
#path_to_img = "./images/thermal-imaging-deers.jpg"

img = io.imread(path_to_img)

used_system = luminance_threshold_based_system.luminance_threshold_based_system
# used_system = information_entropy_based_system.information_entropy_based_system
# used_system = contour_based_system.contour_based_system
used_system.search_for_target(img, True, True)

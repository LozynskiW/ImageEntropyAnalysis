from skimage import io
from image_processing.ready_to_use_systems import information_entropy_based_system, contour_based_system, luminance_threshold_based_system

path_to_img = "C:/Users/wlozy/Pictures/wygaszacze_ekranu/wanderer-above-the-sea-of-fog-by-caspar-david-friedrich-wallpaper.jpg"
img = io.imread(path_to_img)

used_system = luminance_threshold_based_system.luminance_threshold_based_system
# used_system = information_entropy_based_system.information_entropy_based_system
# used_system = contour_based_system.contour_based_system
used_system.search_for_target(img, True, True)

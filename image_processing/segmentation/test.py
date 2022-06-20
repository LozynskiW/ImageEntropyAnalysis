from threshold import information_threshold, simple_luminance_threshold
from skimage import io

img = io.imread('D:/artykuly/wat_2/test_animations/deer/h20m_r20m/0016.png')

simple_luminance_threshold_test = simple_luminance_threshold(min_luminance_threshold=100,
                                                             verbose_mode=True,
                                                             show_image_after_processing=True)

simple_luminance_threshold_test.segmentation(img=img)

information_threshold_test = information_threshold(max_std_dev_from_mean=1, verbose_mode=True, show_image_after_processing=True)
information_threshold_test.segmentation(img=img)

"""
contour_segmentation(img=img, method='canny',
                     verbose_mode=True, show_image_after_processing=True)
                     
"""

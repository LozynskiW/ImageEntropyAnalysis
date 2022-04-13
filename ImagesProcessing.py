import random
from matplotlib import pyplot as plt
import numpy as np
from pyitlib import discrete_random_variable as drv
import InformationGainAnalysis.InformationEntropyAnalysis
import ImageEntropyAnalysis
from skimage import filters as filter
from skimage import feature, img_as_uint, img_as_ubyte, exposure
from skimage.filters.rank import median, mean_bilateral
from skimage import io
from skimage.color import rgb2grey, rgb2gray
from skimage.morphology import disk, ball
from InformationGainAnalysis.DataStorage import LocalDataStorage

localStorageTest = LocalDataStorage()
localStorageTest.set_main_folder('D:/magisterka/antrax')
localStorageTest.set_object('sarna')
print(localStorageTest.get_folder_contents())

for i in localStorageTest.get_folder_contents():
    localStorageTest.set_dataset(i)
    localStorageTest.list_dataset_contents()

img = io.imread('C:/Users/Wojciech Łożyński/Desktop/WAT/magisterka/materiały/termowizja/termo/wybrane/daniel/resized8bit/IM_49_res.jpg')
img2 = io.imread('C:/Users/Wojciech Łożyński/Desktop/WAT/magisterka/materiały/termowizja/termo/wybrane/sarna/resized8bit/IM_731_res.jpg')
img_dzik = io.imread('C:/Users/Wojciech Łożyński/Desktop/WAT/magisterka/materiały/termowizja/termo/wybrane/dzik/resized8bit/1/DJI_0001_res.jpg')
img_drzewo = io.imread('D:/magisterka/antrax/dzik/2021-02-23T235735/2021 02 23 23 57 35 001.tiff')
img = io.imread('D:/magisterka/antrax/dzik/2021-02-23T235735/2021 02 24 00 04 16 002.tiff')
test_log = {
            "time": 0,
            "longitude": 0,
            "latitude": 0,
            "gps_height": 100,
            "barometric_height": 80,
            "pitch": 30,
            "roll": 30,
            "yaw": 30,
            "gps_speed": 0,
            "gps_course": 0,
        }
img_dzik = rgb2gray(img_dzik)
img_dzik = img_as_ubyte(img_dzik)

img2 = rgb2gray(img2)
img2 = img_as_ubyte(img2)

img_gray = rgb2gray(img)
img_gray = img_as_ubyte(img_gray)

original_im_histogram = InformationGainAnalysis.InformationEntropyAnalysis.StatisticsParameters()
object_finder = InformationGainAnalysis.InformationEntropyAnalysis.ImageInformationAnalysis()
object_finder.add_histogram_filtering_data(255,255)

grayscale, original_histogram = original_im_histogram.image_histogram(img_gray, 'on')
original_im_entropy, _, _ = original_im_histogram.information_entropy(img_gray)

img_canny = ImageEntropyAnalysis.feature.canny(img_gray, sigma=1)
#img_thresh = ImageEntropyAnalysis.threshold_segmentation(img_gray, 100)
#_, thresh_histogram = original_im_histogram.image_histogram(img_thresh, 'on')

"""Noise adding"""

img_noisy = img_gray.copy()

szer = len(img_gray[0])
wys = len(img_gray)

for x in range(0, szer):
    for y in range(0, wys):
        if random.randrange(100) > 95:
            img_noisy[y][x] = img_noisy[y][x] * 20

_, noisy_histogram = original_im_histogram.image_histogram(img_noisy, "on")
noisy_im_entropy, _, _ = original_im_histogram.information_entropy(img_noisy)

img_gauss_filtered = img_as_ubyte(filter.gaussian(img_noisy, 3))

gauss_im_entropy, _, _ = original_im_histogram.information_entropy(img_gauss_filtered)
_, gauss_histogram = original_im_histogram.image_histogram(img_gauss_filtered, "on")

img_median_filtered = img_as_ubyte(median(img_noisy, disk(1)))
median_im_entropy, _, _ = original_im_histogram.information_entropy(img_median_filtered)
_, median_histogram = original_im_histogram.image_histogram(img_median_filtered, "on")

img_bilateral_filtered = img_as_ubyte(mean_bilateral(img_noisy, disk(5), s0=10, s1=10))
bilateral_im_entropy, _, _ = original_im_histogram.information_entropy(img_bilateral_filtered)
_, bilateral_histogram = original_im_histogram.image_histogram(img_bilateral_filtered, "on")

information_mutual_original_noisy = np.round(drv.information_mutual(original_histogram, noisy_histogram), 2)
information_mutual_original_noisy_filtered_by_gauss = np.round(drv.information_mutual(original_histogram, gauss_histogram), 2)
information_mutual_original_noisy_filtered_by_median = np.round(drv.information_mutual(original_histogram, median_histogram), 2)
information_mutual_original_noisy_filtered_by_bilateral = np.round(drv.information_mutual(original_histogram, bilateral_histogram), 2)

object_finder.add_image(img)
object_finder.image_entropy_analysis_for_testing(None)
img_detected = object_finder.get_image()

object_finder.add_image(img2)
object_finder.image_entropy_analysis_for_testing(None)
img_detected2 = object_finder.get_image()

object_finder.add_image(img_dzik)
object_finder.image_entropy_analysis_for_testing(None)
img_dzik = object_finder.get_image()

_, sarna_wzor_histogram = original_im_histogram.image_histogram_with_offset(img_detected, normalize="on", grayscale_offset=1)
_, sarna_test_histogram = original_im_histogram.image_histogram_with_offset(img_detected2, normalize="on", grayscale_offset=1)
_, dzik_histogram = original_im_histogram.image_histogram_with_offset(img_dzik, normalize="on", grayscale_offset=1)
print('I(sarna|sarna)=', np.round(drv.information_mutual(sarna_wzor_histogram, sarna_test_histogram), 2))
print('I(dzik|sarna)=', np.round(drv.information_mutual(sarna_wzor_histogram, dzik_histogram), 2))
"""
fig, axs = plt.subplots(3, 2, figsize=(3,6))

axs[0, 0].bar(grayscale, bilateral_histogram)
axs[0, 1].imshow(img_bilateral_filtered, cmap="gray")

axs[0, 0].set_title('Histogram obrazu')
axs[0, 1].set_title('Filtr bilateralny')
axs[0, 0].set_xlabel("H(Y)="+str(bilateral_im_entropy))
axs[0, 1].set_xlabel("I(X|Y)="+str(information_mutual_original_noisy_filtered_by_bilateral))

axs[1, 0].bar(grayscale, gauss_histogram)
axs[1, 1].imshow(img_gauss_filtered, cmap="gray")
axs[1, 1].set_title('Filtr gaussa')
axs[1, 0].set_xlabel("H(Y)="+str(gauss_im_entropy))
axs[1, 1].set_xlabel("I(X|Y)="+str(information_mutual_original_noisy_filtered_by_gauss))

axs[2, 0].bar(grayscale, median_histogram)
axs[2, 1].imshow(img_median_filtered, cmap="gray")
axs[2, 1].set_title('Filtr medianowy')
axs[2, 0].set_xlabel("H(Y)="+str(median_im_entropy))
axs[2, 1].set_xlabel("I(X|Y)="+str(information_mutual_original_noisy_filtered_by_median))

fig2, axs2 = plt.subplots(3, 1, figsize = (3,6))
axs2[0].imshow(img, cmap="gray")
axs2[1].bar(grayscale, original_histogram)
axs2[2].imshow(img_noisy, cmap="gray")
axs2[2].set_xlabel("H(X)="+str(original_im_entropy))
axs2[0].set_ylabel("P(x)")
axs2[2].set_ylabel("P(x)")
"""
fig, axs = plt.subplots(3, 2)

axs[0, 0].bar(grayscale, sarna_wzor_histogram)
axs[0, 1].imshow(img_detected, cmap="gray")

axs[0, 0].set_ylabel('#1', fontsize=25)

axs[1, 0].bar(grayscale, sarna_test_histogram)
axs[1, 1].imshow(img_detected2, cmap="gray")

axs[1, 0].set_ylabel('#2', fontsize=25)

axs[2, 0].bar(grayscale, dzik_histogram)
axs[2, 1].imshow(img_dzik, cmap="gray")

axs[2, 0].set_ylabel('#3', fontsize=25)

plt.show()


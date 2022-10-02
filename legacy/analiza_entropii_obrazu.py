import ImageEntropyAnalysis
from skimage import feature, img_as_ubyte
from skimage import io
from skimage.color import rgb2grey

"""
hardkorowe: 600 1298
"""
img = io.imread('C:/Users/Wojciech Łożyński/Desktop/WAT/magisterka/materiały/termowizja/termo/_wybrane_/daniel/resized8bit/IM_800_res.jpg')
#ImageEntropyAnalysis.show_image(img)

img_gray = rgb2grey(img)
img_gray = img_as_ubyte(img_gray)

"""Test histogramu"""

ImageEntropyAnalysis.show_image(img_gray)

edges2 = feature.canny(img_gray, sigma=2)
ImageEntropyAnalysis.show_image(edges2)

#clip_path = 'C:/Users/Wojciech Łożyński/Desktop/WAT/magisterka/materiały/termowizja/kojot_avi.avi'
#im = image.imread('C:/Users/Wojciech Łożyński/Desktop/WAT/magisterka/materiały/termowizja/termo/_wybrane_/daniel/resized8bit/IM_136_res.jpg')
#print(im.dtype, im.shape, type(im))
#im_copy = im.copy()
#im_low = ImageEntropyAnalysis.low_high_pass_filter(im_copy, "low", 5)
#im_high = ImageEntropyAnalysis.low_high_pass_filter(im_copy, "high", 5)

im_copy = ImageEntropyAnalysis.information_threshold(img_gray)
ImageEntropyAnalysis.show_image(im_copy)
#ImageEntropyAnalysis.show_image(im_copy)

#im_test = ImageEntropyAnalysis.test(im_copy, im_low)
#im_test = ImageEntropyAnalysis.test(im_copy, im_high)

im_copy = ImageEntropyAnalysis.search_for_object(im_copy, edges2)
ImageEntropyAnalysis.show_image(im_copy)
#T = ImageEntropyAnalysis.otsu_threshold(im)
#im = ImageEntropyAnalysis.threshold_segmentation(im, T)
#ImageEntropyAnalysis.image_deldensity(im)
#x, y, H, Hn, In = ImageEntropyAnalysis.information_entropy(im)
#d3_H = ImageEntropyAnalysis.entropy3d_view(In, im_copy, 'on')

#ImageEntropyAnalysis.information_data_comparision(im, im_copy)

#ImageEntropyAnalysis.entropy_video_analysis(clip_path)

"""
animal = 'sarna'

dzik_path = 'C:/Users/Wojciech Łożyński/Desktop/WAT/magisterka/materiały/termowizja/termo/_wybrane_/dzik/resized8bit/1/'
sarna_path = 'C:/Users/Wojciech Łożyński/Desktop/WAT/magisterka/materiały/termowizja/termo/_wybrane_/sarna/resized8bit/'
daniel_path = 'C:/Users/Wojciech Łożyński/Desktop/WAT/magisterka/materiały/termowizja/termo/_wybrane_/daniel/resized8bit/'

histogram_analysis = ImageEntropyAnalysis.HistogramAnalyser()
histogram_analysis.set_result_path("C:\\Users\\Wojciech Łożyński\\Desktop\\WAT\\magisterka\\program\\results\\")
#histogram_analysis.create_new_data('sarna', 'IM_', path, 100)
histogram_analysis.load_data(animal)
#histogram_analysis.analyse_database('IM_', path, 100)
print("Is histogram valid: ", histogram_analysis.check_saved_histogram())
print("Are histograms similar? ", histogram_analysis.check_histograms_match(io.imread(sarna_path+"IM_1_res.jpg")))

"""



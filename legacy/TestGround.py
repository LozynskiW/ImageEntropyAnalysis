import numpy as np
import ImageEntropyAnalysis
from skimage import img_as_ubyte
from skimage import io
from skimage.color import rgb2grey
import matplotlib.pyplot as plt
from legacy import InformationEntropyAnalysis

InformationEntropyAnalysisTest = InformationEntropyAnalysis.ImageInformationAnalysis()

"""
lajtowe: 31
hardkorowe: 1298, 498
C:/Users/Wojciech Łożyński/Desktop/WAT/magisterka/materiały/termowizja/termo/wybrane/daniel/resized8bit/IM_31_res.jpg
img = io.imread('D:/magisterka/antrax/2021-02-04T182803/2021 02 04 18 28 29 263.tif')
"""
img = io.imread('D:/magisterka/antrax/sarna/2021-02-04T211617/2021 02 04 21 16 17 812.tif')
img2 = io.imread('C:/Users/Wojciech Łożyński/Desktop/WAT/magisterka/materiały/termowizja/termo/wybrane/daniel/resized8bit/IM_1298_res.jpg')
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
img_gray = rgb2grey(img)
img_gray = img_as_ubyte(img_gray)

InformationEntropyAnalysisTest.add_image(img_gray)
InformationEntropyAnalysisTest.image_entropy_analysis_for_testing(test_log)

img_gray2 = rgb2grey(img2)
img_gray2 = img_as_ubyte(img_gray2)


grayscale, grayscale_prob = ImageEntropyAnalysis.image_histogram(img_gray, "on")
grayscale_test, grayscale_prob_test = ImageEntropyAnalysis.image_histogram(img_gray2, "on")

_, gray_shade_prob, H, H_n, I_n= ImageEntropyAnalysis.information_entropy(img)
print(np.average(I_n, weights=gray_shade_prob))
plt.bar(grayscale, I_n)
plt.show()

img_mean_value = ImageEntropyAnalysis.mean_from_probability(grayscale, grayscale_prob)
img2_mean_value = ImageEntropyAnalysis.mean_from_probability(grayscale_test, grayscale_prob_test)

_, _, im_entropy, _, _ = ImageEntropyAnalysis.information_entropy(img_gray)
_, _, im2_entropy, _, _ = ImageEntropyAnalysis.information_entropy(img_gray2)
#print('Im1 = ', img_mean_value, 'Im1 H = ', im_entropy)
#print('Im2 = ', img2_mean_value, 'Im2 H = ', im2_entropy)

"""
json_test = [{
    "id": "1",
    "dtype": str(img_gray.dtype),
    "histogram": str(grayscale_prob)
    },{
    "id": "2",
    "dtype": str(img_gray.dtype),
    "histogram": str(grayscale_prob)
}]

with open("json_test.json","w") as write_file:
    json.dump(json_test, write_file)
write_file.close()
with open("json_test.json", "r") as read_file:
    data = json.load(read_file)
read_file.close()


kernel = np.array([[-1, -1, -1, -1, -1],
                   [-1,  1,  2,  1, -1],
                   [-1,  2,  4,  2, -1],
                   [-1,  1,  2,  1, -1],
                   [-1, -1, -1, -1, -1]])
highpass_5x5 = ndimage.convolve(img_adapteq, kernel)
ImageEntropyAnalysis.show_image(highpass_5x5)
"""

"""
edges2 = feature.canny(img_gray, sigma=2)
ImageEntropyAnalysis.show_image(edges2)
im_copy = ImageEntropyAnalysis.information_threshold(img_gray)
ImageEntropyAnalysis.show_image(im_copy)
im_copy = ImageEntropyAnalysis.search_for_object(im_copy, edges2)
ImageEntropyAnalysis.show_image(im_copy)
"""

processed_img = InformationEntropyAnalysisTest.get_image()

fig, axs = plt.subplots(2,2)
fig.suptitle('Comparison')

grayscale_test, grayscale_prob_test = ImageEntropyAnalysis.image_histogram(processed_img, "on")
axs[0, 0].bar(grayscale, grayscale_prob)
axs[0, 1].imshow(img_gray, cmap="gray")
axs[1, 0].bar(grayscale_test, grayscale_prob_test)
axs[1, 1].imshow(processed_img, cmap="gray")
plt.show()
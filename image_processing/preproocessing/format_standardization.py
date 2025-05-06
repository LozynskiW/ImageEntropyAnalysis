from image_processing.preproocessing import preprocessing_interfaces
from skimage.util import img_as_ubyte
from skimage.color import rgb2gray
import numpy as np


class to_unit8_rgb(preprocessing_interfaces.base):

    def process_img(self, img):
        if super().verbose_mode: print("Initiating format check...", end="")

        try:
            self.__img_format_check(img)
        except ValueError:
            if super().verbose_mode: print("format invalid, converting image")
            return self.__convert_img(img)
        else:
            if super().verbose_mode: print("format valid")
            return img

    @staticmethod
    def __convert_img(img):
        print("IMG in __convert_img")
        print(img)
        img = rgb2gray(img)
        return img_as_ubyte(img)

    @staticmethod
    def __img_format_check(img):

        if type(img[0][0]) != np.uint8:
            print("Type of image:", type(img[0][0]))
            raise ValueError("Img must be in uint format for example: uint8 = 256 bits for luminance values")


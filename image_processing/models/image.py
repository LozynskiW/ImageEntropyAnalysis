from abc import ABC

import numpy as np
from numpy import ndarray
from skimage.util import img_as_ubyte
from skimage.color import rgb2gray


class ArrayImage:
    image_array: ndarray

    def __init__(self, image):
        if not isinstance(image, np.ndarray):
            raise ValueError("passed image is not numpy.ndarray")
        if len(image.shape) != 2:
            raise ValueError("passed image is not 2d")
        self.image_array = image

    def __getitem__(self, index):
        return self.image_array[index]

    def __len__(self):
        return len(self.image_array)


class GrayscaleImage8bit(ArrayImage, ABC):

    def __init__(self, image):
        if image[0][0] is not None and image[0][0].dtype != np.uint8:
            raise ValueError("passed image is not 8bit grayscale, should be numpy.uint8")
        super().__init__(image)

    @staticmethod
    def from_image(any_image):
        img_converted = img_as_ubyte(rgb2gray(any_image))
        return GrayscaleImage8bit(img_converted)

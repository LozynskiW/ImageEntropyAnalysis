import numpy as np

from image_processing.basictools import twodimstructures


class validation_correction:

    def __init__(self, verbose_mode):
        self.__verbose_mode = verbose_mode

    @staticmethod
    def is_image_vignetted(img):

        height = len(img)
        width = len(img[0])

        nrows, ncols = img.shape
        row, col = np.ogrid[:nrows, :ncols]
        cnt_row, cnt_col = nrows / 2, ncols / 2
        outer_disk_mask = ((row - cnt_row) ** 2 + (col - cnt_col) ** 2 > (nrows / 2) ** 2)

        outer_disk_pixels = []
        inner_disk_pixels = []

        for y in range(0, height):
            for x in range(0, width):
                if outer_disk_mask[y][x]:
                    outer_disk_pixels.append(img[y][x])
                else:
                    inner_disk_pixels.append(img[y][x])

        if np.mean(outer_disk_pixels) > np.mean(inner_disk_pixels) + 0.2 * np.mean(outer_disk_pixels):
            return True

        return False

    def process_img(self, img):

        if self.__verbose_mode: print("")
        if self.__verbose_mode: print("vignetting_correction")
        if self.__verbose_mode: print("---------------------")

        if self.__verbose_mode: print("Checking if img is vignetted...")

        if self.is_image_vignetted(img):
            if self.__verbose_mode: print("Img is vignetted, vignetting correction initiated...", end="")

            rows, cols = img.shape[:2]

            resultant_kernel = twodimstructures.calculate_gaussian_kernel(cols, rows)

            mask = 255 * resultant_kernel / np.linalg.norm(resultant_kernel)
            img = np.uint8(img * mask)

            if self.__verbose_mode: print("DONE")
            return img

        return img
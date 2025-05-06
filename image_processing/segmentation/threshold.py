from copy import deepcopy

from image_processing.segmentation import segmentation_interfaces
from pylab import *

import image_processing.basictools.statisticalparameters as img_stat


class information_threshold(segmentation_interfaces.base):

    def __init__(self, verbose_mode, show_image_after_processing, max_std_dev_from_mean=1):

        super().__init__(
            verbose_mode=verbose_mode,
            show_image_after_processing=show_image_after_processing
        )
        self.__max_std_dev_from_mean = max_std_dev_from_mean

    def segmentation(self, img):
        """
        Metoda pozwalająca na segmentowanie obrazu poprzez progowanie. Próg obliczany jest na podstawie informacyjności
        poszczególnych odcieni szarości z przestrzeni barw (skali szarości). Warunkiem pozostawienia piksela jest wartość
        informacyjności powyżej średniej
        :param img:
        :return:
        """

        if super().verbose_mode:
            print("")
            print("information_threshold_segmentation")
            print("----------------------------------")
            print("Beginning")

        img_width = len(img[0])
        img_height = len(img)

        _, weights = img_stat.image_histogram(img, normalize_to_pdf=True)

        information_per_luminance = img_stat.information(img)

        entropy, entropy_per_luminance = img_stat.information_entropy(img)

        std_of_information = np.std(information_per_luminance)

        if super().verbose_mode:
            print("")
            print("calculated image statistical parameters")
            print("mean value from histogram:", mean(weights))
            print("mean information per luminance: ", mean(information_per_luminance))
            print("entropy: ", entropy)
            print("std of information: ", std_of_information)

        img_after_processing = img.copy()

        for x in range(0, img_width):

            for y in range(0, img_height):

                if information_per_luminance[img[y][x]] < entropy + self.__max_std_dev_from_mean * std_of_information:
                    img_after_processing[y][x] = 0
                else:
                    img_after_processing[y][x] = 255

        if super().verbose_mode:
            print("")
            print("DONE")

        if super().show_image_after_processing:
            super().show_images(imgs_before=img,
                                img_after=img_after_processing,
                                fig_title="Image after information threshold segmentation")

        return img_after_processing


class simple_luminance_threshold(segmentation_interfaces.threshold):

    def segmentation(self, img):

        if super().verbose_mode:
            print("")
            print("luminance_threshold_segmentation")
            print("--------------------------------")
            print("Beginning")

        img_width = len(img[0])
        img_height = len(img)

        img_after_processing = deepcopy(img)

        for x in range(0, img_width):

            for y in range(0, img_height):

                if img[y][x] < super().get_min_luminance_threshold():
                    img_after_processing[y][x] = 0
                else:
                    img_after_processing[y][x] = 255

        if super().verbose_mode:
            print("")
            print("DONE")

        if super().show_image_after_processing:
            super().show_images(imgs_before=(img, img),
                                img_after=img_after_processing,
                                fig_title="Image simple luminance threshold segmentation")

        return img_after_processing

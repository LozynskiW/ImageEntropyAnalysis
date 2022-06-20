import numpy as np

from InformationGainAnalysis.image_processing.basictools.utilities import show_images_before_and_after, \
    show_image_before_and_after


class verbose_mode:

    def __init__(self, verbose_mode):
        self.__verbose_mode = verbose_mode

    @property
    def verbose_mode(self):
        return self.__verbose_mode

    @verbose_mode.setter
    def verbose_mode(self, verbose_mode):
        self.__verbose_mode = verbose_mode


class show_img_before_and_after_with_verbose_mode(verbose_mode):

    def __init__(self, verbose_mode, show_image_after_processing):
        super().__init__(verbose_mode)
        self.__show_image_after_processing = show_image_after_processing

    @property
    def show_image_after_processing(self):
        return self.__show_image_after_processing

    @show_image_after_processing.setter
    def show_image_after_processing(self, show_image_after_processing):
        self.__show_image_after_processing = show_image_after_processing

    @staticmethod
    def show_images(imgs_before, img_after, fig_title):

        if type(imgs_before[0][0]) in [np.uint8, int, float]:

            show_image_before_and_after(img_before_processing=imgs_before,
                                        img_after_processing=img_after,
                                        fig_title=fig_title)
        else:
            show_images_before_and_after(imgs_before_processing=imgs_before,
                                         img_after_processing=img_after,
                                         fig_title=fig_title)

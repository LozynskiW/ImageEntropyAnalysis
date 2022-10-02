from app.image_processing.validation.validation_interfaces import base
from app.image_processing.basictools import statisticalparameters as stat_params


class maximal_mean_luminance(base):

    def __init__(self, validating_mean, validating_std, deviation_from_mean_in_std, verbose_mode):
        super().__init__(verbose_mode)
        self.__validating_mean = validating_mean
        self.__validating_std = validating_std
        self.__deviation_from_mean_in_std = deviation_from_mean_in_std

    def validate(self, img):

        if super().verbose_mode:
            print("")
            print("maximal_mean_luminance")
            print("--------------------")
            print("Beginning")
        grayscale, grayscale_prob = stat_params.image_histogram(im=img, normalize_to_pdf=True)

        mean_pixel_value = stat_params.exp_val_from_histogram(grayscale, grayscale_prob)

        if super().verbose_mode:
            print("")
            print("mean_pixel_value = ", mean_pixel_value)
            print("mean_luminance_limit = ",
                  self.__validating_mean + self.__deviation_from_mean_in_std * self.__validating_std)

        if mean_pixel_value < self.__validating_mean + self.__deviation_from_mean_in_std * self.__validating_std:
            if super().verbose_mode:
                print("Image valid")
            return True

        if super().verbose_mode:
            print("Image invalid")

        return False

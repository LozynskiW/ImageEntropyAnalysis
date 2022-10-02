from app.image_processing.basictools.BasicTools import TwoDimStructures, calculate_fill_factor
from app.image_processing.postprocessing import postprocessing_interfaces
from app.image_processing.basictools.utilities import show_image


class fill_factor_based(postprocessing_interfaces.base):

    def validate_or_process(self, img, fill_factor):

        if self.verbose_mode:
            print("Validating...")

        if not self.__validate(fill_factor=fill_factor):
            img = self.img_noise_outside_centre_deleting(img)
            fill_factor = calculate_fill_factor(img=img)

            if self.verbose_mode:
                print("fill_factor: ",fill_factor, "/",self.max_fill_factor)
                print("not valid")

            return self.__validate(fill_factor), img, fill_factor
        else:
            if self.verbose_mode:
                print("valid")

            return True, img, fill_factor

    def __validate(self, fill_factor):

        return super().max_fill_factor > fill_factor

    @staticmethod
    def img_noise_outside_centre_deleting(img):

        center_disk_mask = TwoDimStructures.center_disk_mask(img, size_factor=3)

        width = len(img[0])
        height = len(img)

        for y in range(0, height):
            for x in range(0, width):

                if center_disk_mask[y][x]:
                    img[y][x] = 0

        return img
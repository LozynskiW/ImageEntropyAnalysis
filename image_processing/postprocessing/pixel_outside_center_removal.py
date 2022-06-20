from InformationGainAnalysis.image_processing.basictools.BasicTools import TwoDimStructures, calculate_fill_factor
from InformationGainAnalysis.image_processing.postprocessing import postprocessing_interfaces


class fill_factor_based(postprocessing_interfaces.base):

    def validate_or_process(self, img, fill_factor):

        if not self.__validate(fill_factor=fill_factor):
            img = self.img_noise_outside_centre_deleting(img)
            fill_factor = calculate_fill_factor(img=img)

            return self.__validate(fill_factor), img, fill_factor
        else:
            return True, img, fill_factor

    def __validate(self, fill_factor):

        return super().max_fill_factor > fill_factor

    @staticmethod
    def img_noise_outside_centre_deleting(img):

        center_disk_mask = TwoDimStructures.center_disk_mask(img)

        width = len(img[0])
        height = len(img)

        for y in range(0, height):
            for x in range(0, width):

                if not center_disk_mask[y][x]:
                    img[y][x] = 0

        return img
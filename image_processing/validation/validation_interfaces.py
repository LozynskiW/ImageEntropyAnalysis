from image_processing.interfaces import verbose_mode


class ImageValidator(verbose_mode):

    def validate(self, img):
        return NotImplementedError
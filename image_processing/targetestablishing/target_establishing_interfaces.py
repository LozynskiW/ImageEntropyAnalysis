from app.image_processing.interfaces import verbose_mode


class base(verbose_mode):

    def establish_target_location(self, target_coordinates):
        raise NotImplementedError

from abc import ABC

from InformationGainAnalysis.image_processing.basictools.imageoverlay import image_add, image_and, image_multiply
from InformationGainAnalysis.image_processing.basictools.utilities import calculate_fill_factor
from InformationGainAnalysis.image_processing.interfaces import show_img_before_and_after_with_verbose_mode


class add(show_img_before_and_after_with_verbose_mode, ABC):

    def __init__(self, verbose_mode, show_image_after_processing):

        super().__init__(verbose_mode, show_image_after_processing)

    def fuse(self, imgs):

        img = imgs[0]

        for i in range(1, len(imgs) - 1):
            img = image_add(img=img, mask=imgs[i])

        if super().show_image_after_processing:
            super().show_images(imgs_before=imgs, img_after=img, fig_title="Image after fusing")

        return img, calculate_fill_factor(img=img)


class multiply(show_img_before_and_after_with_verbose_mode, ABC):

    def __init__(self, verbose_mode, show_image_after_processing):

        super().__init__(verbose_mode, show_image_after_processing)

    def fuse(self, imgs):

        img = imgs[0]

        for i in range(1, len(imgs) - 1):
            img = image_multiply(img=img, mask=imgs[i])

        if super().show_image_after_processing:
            super().show_images(imgs_before=imgs, img_after=img, fig_title="Image after fusing")

        return img, calculate_fill_factor(img=img)


class im_and(show_img_before_and_after_with_verbose_mode, ABC):

    def __init__(self, verbose_mode, show_image_after_processing):

        super().__init__(verbose_mode, show_image_after_processing)

    def fuse(self, imgs):

        img = imgs[0]

        for i in range(1, len(imgs) - 1):
            img = image_and(img=img, mask=imgs[i])

        if super().show_image_after_processing:
            super().show_images(imgs_before=imgs, img_after=img, fig_title="Image after fusing")

        return img, calculate_fill_factor(img=img)

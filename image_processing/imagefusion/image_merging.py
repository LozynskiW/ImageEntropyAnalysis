from abc import ABC

from image_processing.basictools.imageoverlay import image_add, image_and, image_multiply
from image_processing.basictools.utilities import calculate_fill_factor


class add:

    def __init__(self, verbose_mode, show_image_after_processing):
        pass

    def fuse(self, imgs):

        img = imgs[0]

        for i in range(1, len(imgs) - 1):
            img = image_add(img=img, mask=imgs[i])

        if super().show_image_after_processing:
            super().show_images(imgs_before=imgs, img_after=img, fig_title="Image after fusing")

        return img, calculate_fill_factor(img=img)


class multiply:

    def __init__(self, verbose_mode, show_image_after_processing):
        pass

    def fuse(self, imgs):

        img = imgs[0]

        for i in range(1, len(imgs) - 1):
            img = image_multiply(img=img, mask=imgs[i])

        if super().show_image_after_processing:
            super().show_images(imgs_before=imgs, img_after=img, fig_title="Image after fusing")

        return img, calculate_fill_factor(img=img)


class im_and:

    def __init__(self, verbose_mode, show_image_after_processing):
        pass

    def fuse(self, imgs):

        img = imgs[0]

        for i in range(1, len(imgs) - 1):
            img = image_and(img=img, mask=imgs[i])

        if super().show_image_after_processing:
            super().show_images(imgs_before=imgs, img_after=img, fig_title="Image after fusing")

        return img, calculate_fill_factor(img=img)

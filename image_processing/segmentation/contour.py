from pylab import *
from skimage import feature
from skimage.segmentation import flood
from image_processing.segmentation import segmentation_interfaces

from image_processing.validation import contour_closure


class canny(segmentation_interfaces.base):

    def segmentation(self, img, sigma=4):

        img_after_processing = img.copy()

        contour_closure_validator = contour_closure.without_contour_closing(verbose_mode=False)

        if super().verbose_mode:
            print("")
            print("contour_segmentation")
            print("--------------------")
            print("Beginning")
            print("Sigma = ", sigma)

        img_after_processing = feature.canny(img_after_processing, sigma=sigma)

        if contour_closure_validator.validate(img=img_after_processing):
            if super().verbose_mode: print("Contour is closed")
            img_after_processing = flood(img_after_processing, (1, 1), connectivity=1)
        else:
            if super().verbose_mode:
                if sigma > 1:
                    print("Contour not closed, trying another time with sigma=", sigma)
                    self.segmentation(img=img, sigma=sigma - 1)

                else:
                    print("Unable to detect target")
                    return img_after_processing

        if super().show_image_after_processing:
            super().show_images(imgs_before=img,
                                img_after=img_after_processing,
                                fig_title="Image after contour segmentation, sigma=" + str(sigma))

        return img_after_processing

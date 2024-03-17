from skimage.segmentation import flood
from image_processing.validation import validation_interfaces


class without_contour_closing(validation_interfaces.base):
    """
    Klasa pozwalająca na okreslenie, czy kontur obiektu jest zamknięty
    """

    def __init__(self, verbose_mode):
        super().__init__(verbose_mode)
        self.__img = None
        self.__szer = 0
        self.__wys = 0

    def __set_img(self, contour_segmented_img):
        self.__img = contour_segmented_img
        self.__szer = len(self.__img[0])
        self.__wys = len(self.__img)

    def validate(self, img):

        self.__set_img(img)

        if self.check_if_contour_is_closed() and self.check_if_contour_exist():
            return True

        return False

    def check_if_contour_is_closed(self):

        coords = self.__hook_to_pixel()

        if not coords:
            return False

        object_area = self.__enlarge_window(coords[0], coords[1])

        original_num = self.__count_white_pixels_in_given_area(object_area[0],
                                                               object_area[1],
                                                               object_area[2],
                                                               object_area[3],
                                                               True)

        self.__img = flood(self.__img, (0, 0), connectivity=0)

        if self.__count_white_pixels_in_given_area(object_area[0], object_area[1], object_area[2], object_area[3],
                                                   False) > original_num:
            return True

        return False

    def check_if_contour_exist(self):
        for y in range(0, self.__wys):
            for x in range(0, self.__szer):
                if self.__img[y][x]:
                    return True
        return False

    def __hook_to_pixel(self):
        for y in range(0, self.__wys):
            for x in range(0, self.__szer):
                if self.__img[y][x]:
                    return [y, x]
        return []

    def __count_white_pixels_in_given_area(self, corner_y, corner_x, height, width, test):
        num = 0
        for y in range(corner_y, corner_y + height):
            for x in range(corner_x, corner_x + width):
                try:
                    if self.__img[y][x] == test:
                        num += 1
                except IndexError:
                    continue
        return num

    def __enlarge_window(self, pixel_y, pixel_x):

        window_height = 1
        window_width = 1
        pixel_count = 1

        while True:

            window_height += 1
            window_width += 1

            if self.__count_white_pixels_in_given_area(pixel_y, pixel_x, window_height, window_width,
                                                       True) > pixel_count:
                pixel_count = self.__count_white_pixels_in_given_area(pixel_y, pixel_x, window_height, window_width,
                                                                      True)
            else:
                break

        while True:

            pixel_x -= 1
            pixel_y -= 1

            if self.__count_white_pixels_in_given_area(pixel_y, pixel_x, window_height, window_width,
                                                       True) > pixel_count:
                pixel_count = self.__count_white_pixels_in_given_area(pixel_y, pixel_x, window_height, window_width,
                                                                      True)
            else:
                break

        return [pixel_y, pixel_x, window_height, window_width]

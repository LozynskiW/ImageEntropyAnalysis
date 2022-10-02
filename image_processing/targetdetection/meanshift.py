from app.image_processing.basictools.utilities import show_detected_target_on_img

from app.image_processing.targetdetection import targetdetection_interfaces


class highest_luminance_density(targetdetection_interfaces.base):

    def search_for_target(self, segmented_img):
        if super().verbose_mode:
            print("")
            print("mean_shift")
            print("----------")
            print("Beginning")

        width = len(segmented_img[0])
        height = len(segmented_img)

        window_width = int(width / 40)
        window_height = int(height / 40)

        highest_mean = 0
        obj_x = 0
        obj_y = 0

        for y in range(0, height):
            for x in range(0, width):

                if segmented_img[y][x] > 0:
                    mean = 0
                    num = 0

                    for yw in range(0, window_height):
                        for xw in range(0, window_width):

                            try:
                                mean += segmented_img[y + yw][x + xw]
                            except:
                                mean += 0
                            finally:
                                num += 1

                    mean = mean / num

                    if mean > highest_mean:
                        highest_mean = mean
                        obj_x = x
                        obj_y = y

        if super().verbose_mode:
            print("Auto search window fitting initiated...", end="")
        obj_x, obj_y, window_height, window_width = self.__auto_window_fitting(segmented_img=segmented_img,
                                                                               target_x=obj_x,
                                                                               target_y=obj_y,
                                                                               window_height=window_height,
                                                                               window_width=window_width)

        if super().verbose_mode:
            print("DONE")

        if super().verbose_mode:
            print("DONE")
            print("Target x: ", obj_x)
            print("Target y: ", obj_y)
            print("Window height: ", window_height)
            print("Window width: ", window_width)

        if super().show_image_after_processing:
            show_detected_target_on_img(img=segmented_img,
                                        target_x=obj_x,
                                        target_y=obj_y,
                                        window_height=window_height,
                                        window_width=window_width)

        return obj_x, obj_y

    def __auto_window_fitting(self, segmented_img, target_x, target_y, window_height, window_width):
        """Drugi etap - automatyczne rozszerzenie okna"""
        still_search = True
        while still_search:
            still_search = False
            sum = [0, 0]
            num = [0, 0]
            means = [0, 0]
            for yw in range(0, window_height):
                for xw in range(0, window_width):
                    try:
                        if ((xw == 0) and (0 <= yw < window_height)) or ((yw == 0) and (0 <= xw < window_width)):
                            sum[0] += segmented_img[target_y + yw][target_x + xw]
                            num[0] += 1

                        if ((xw == window_width - 1) and (0 <= yw < window_height)) or (
                                (yw == window_height - 1) and (0 <= xw < window_width)):
                            sum[1] += segmented_img[target_y + yw][target_x + xw]
                            num[1] += 1
                    except:
                        still_search = False

            for i in range(0, len(sum)):
                if sum[i] != 0 and num[i] != 0:
                    means[i] = sum[i] / num[i]
                else:
                    means[i] = 0

            if means[0] > 0:
                target_x -= 1
                window_width += 1
                target_y -= 1
                window_height += 1
                still_search = True
            if means[1] > 0:
                window_width += 1
                window_height += 1
                still_search = True

        return target_x, target_y, window_height, window_width
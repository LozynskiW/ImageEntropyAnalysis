import numpy as np
from InformationGainAnalysis.image_processing.targetestablishing import target_establishing_interfaces


class max_target_coordinates_distance(target_establishing_interfaces.base):

    def __init__(self, max_variety, verbose_mode):

        super().__init__(verbose_mode)
        self.__max_variety = max_variety

    def establish_target_location(self, target_coordinates):

        if super().verbose_mode: print("")
        if super().verbose_mode: print("WindowVariety_MeanLocation")
        if super().verbose_mode: print("---------------------")

        if super().verbose_mode: print("Checking if target coordinates are in selected variety...", end="")

        for target_coord1 in target_coordinates:

            for target_coord2 in target_coordinates:

                if (1 - self.__max_variety > target_coord1[0] / target_coord2[0] > 1 + self.__max_variety) or \
                        (1 - self.__max_variety > target_coord1[1] / target_coord2[1] > 1 + self.__max_variety):

                    if super().verbose_mode: print("target inconsistent, not established")
                    return False

        if super().verbose_mode: print("target established")

        mean_x = np.mean(list(map(lambda x: x[0], target_coordinates)))
        mean_y = np.mean(list(map(lambda x: x[1], target_coordinates)))

        if super().verbose_mode: print("Target coordinates: X:", mean_x, " Y:", mean_y)

        return mean_x, mean_y

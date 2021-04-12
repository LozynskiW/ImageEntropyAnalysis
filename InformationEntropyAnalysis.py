from pylab import *
import statistics as stat
from skimage import feature, img_as_ubyte
from skimage import io
from skimage.color import rgb2grey, rgb2gray
from InformationGainAnalysis.ObjectGeoLoc import ObjectGeoLoc
from scipy.stats import norm as norm
from skimage.morphology import closing, convex_hull_object, binary_opening, erosion, flood_fill, skeletonize
from skimage.segmentation import flood
from skimage.util import invert


class ImageInformationAnalysis:
    """
    Klasa służąca do analizowania entropii obrazów termowizyjnych przedstawiających jakiś obiekt. Zdjęcia początkowo
    są segmentowane tak, by pozostały jedynie piksele przedstawiajace poszukiwany obiekt - wyróżniajacy się na tle.
    Przebieg segmentowania:
        1. Obliczenie parametrów statystycznych obrazu -> StatisticalParameters.calculate_all
        2. Segmentacja na podstawie informacyjności -> __information_threshold_segmentation
        3. Segmentacja na podstawie wykrywania krawędzi -> __contour_segmentation
        4. Wykorzystanie położenia pikseli z segmentacji konturowej do obliczania zagęszczenia pikseli w otoczeniu
        lokalizacji piksela na obrazie segmentowanym na podstawie informacyności.
        5. Wybranie lokaliacji o największym zagęsczeniu pikseli - potencjalnie jest to szukany obiekt
        6. Dostosowanie wymiarów bramki wycinającej piksele tak by obejmowała cały obiekt 4-6 -> __search_for_object
    Usuwanie z analizy obrazów prześwietlonych jest niezbędne, ponieważ pozostawienie pikseli obiektu jest mało
    prawdopodobne, ze względu na przesunięcie średniej wartości luminancji pikseli do wartości w których odwozorowane
    są poszukiwane obiekty czyli spada ich informacyjność i nie segmentowanie nie działa prawidłowo
    Obrazy nie są wstępnie przetwarzane lub modyfikowane.
    """

    def __init__(self):
        self.__statistical_parameters_calculator = StatisticsParameters()
        self.__object_geo_loc_calculator = ObjectGeoLoc()
        self.__image_quality_controller = ImageQualityController()
        self.__edge_segmentation_controller = ObjectDetectionTester()
        self.img = None
        self.__entropy_of_image = 0
        self.__entropy_of_segmented_image = 0
        self.__mean_pixel_value = 0
        self.__mean_pixel_value_after_processing = 0
        self.__mean_pixel_value_before_processing = 0
        self.__std_dev = 0
        self.__isValid = False
        self.mean_from_db = 0
        self.std_dev_from_db = 0
        self.__horizontal_angle_dist_from_center = 0
        self.__vertical_angle_dist_from_center = 0
        self.__distance_to_object = 0
        self.__fill_factor = 0
        self.__is_object_detected = False
        self.__histogram = None

    def add_histogram_filtering_data(self, mean_pixel_value=0, std_dev_of_mean=0):
        """
        Metoda służąca do dodania wartości średniej i odchylenia tej wartości lumimnancji piksela, co pozwala
        na ustawienie parametru isValid na false, czyli wykrycie obrazu, który jest prześwietlony i w wyniku
        analizy da niewłaściwe rezultaty. Pozostawienie wartości na domyślnych to tryb wstępengo tworzenia bazy danych,
        czyli parametr isValid będzie w każdym przypadku równy false, służy to wstępnemu oszcowaniu parametrów dla
        każdego obrazu w bazie danych celem ustalenia na ich podstawie średniej wartości luminancji z wszystkich zdjęć
        w danym katalogu
        :param mean_pixel_value:
        :param std_dev_of_mean:
        :return:
        """
        self.mean_from_db = mean_pixel_value
        self.std_dev_from_db = std_dev_of_mean

    def add_image_from_path(self, image_path):
        try:
            image = io.imread(image_path)
        except FileNotFoundError:
            print("No image found")
        else:
            img = self.__validate_image_type(image)
            self.img = img

    def add_image(self, image):
        img = self.__validate_image_type(image)
        self.img = img

    @staticmethod
    def __validate_image_type(img):
        img_gray = rgb2gray(img)
        img_gray = img_as_ubyte(img_gray)
        return img_gray

    def __information_threshold_segmentation(self, std='off'):
        """
        Metoda pozwalająca na segmentowanie obrazu poprzez progowanie. Próg obliczany jest na podstawie informacyjności
        poszczególnych odcieni szarości z przestrzeni barw (skali szarości). Warunkiem pozostawienia piksela jest wartość
        informacyjności powyżej średniej
        :param im:
        :return:
        """
        szer = len(self.img[0])
        wys = len(self.img)
        self.__fill_factor = szer * wys  # wsp wypełnienia obrazu pikselami o wartości powyżej 0
        _, weights = self.__statistical_parameters_calculator.image_histogram(self.img)
        _, _, information_per_pixel_val = self.__statistical_parameters_calculator.information_entropy(self.img)
        # mean_information = stat.mean(information_per_pixel_val)
        mean_information = np.average(information_per_pixel_val, weights=weights)
        std_of_information = np.std(information_per_pixel_val)
        if std == 'on':
            std_switch = 1
        else:
            std_switch = 0
        im = self.img.copy()
        for x in range(0, szer):
            for y in range(0, wys):
                if information_per_pixel_val[self.img[y][x]] < mean_information + std_switch * std_of_information:
                    im[y][x] = 0
                    self.__fill_factor -= 1
        self.__fill_factor /= szer * wys
        return im

    def __information_threshold_segmentation_static(self, img):
        """
        Metoda pozwalająca na segmentowanie obrazu poprzez progowanie. Próg obliczany jest na podstawie informacyjności
        poszczególnych odcieni szarości z przestrzeni barw (skali szarości). Warunkiem pozostawienia piksela jest wartość
        informacyjności powyżej średniej
        :param im:
        :return:
        """
        szer = len(img[0])
        wys = len(img)
        self.__fill_factor = szer * wys  # wsp wypełnienia obrazu pikselami o wartości powyżej 0
        _, weights = self.__statistical_parameters_calculator.image_histogram(img)
        _, _, information_per_pixel_val = self.__statistical_parameters_calculator.information_entropy(img)
        # mean_information = stat.mean(information_per_pixel_val)
        mean_information = np.average(information_per_pixel_val, weights=weights)
        im = img.copy()
        for x in range(0, szer):
            for y in range(0, wys):
                if information_per_pixel_val[img[y][x]] < mean_information:
                    im[y][x] = 0
                    self.__fill_factor -= 1
        self.__fill_factor /= szer * wys
        return im

    def __contour_segmentation(self, method, sigma=2):
        if method == 'canny':
            return feature.canny(self.img, sigma=sigma)
        return None

    def __segment_by_contour(self, im, sigma):

        if sigma > 4:
            return None

        out = feature.canny(im, sigma=sigma)

        self.__edge_segmentation_controller.set_img(out)

        if not self.__edge_segmentation_controller.check_if_contour_is_closed():
            sigma += 1
            print("More POWER!!!")
            self.__segment_by_contour(im, sigma)
        else:
            return out

    @staticmethod
    def __search_for_object(information_segmented_im, edge_segmented_image):
        """
        Metoda do wyszukiwania obiektu na obrazie.
        Działanie: metoda sprawdza położenie pikseli o intensywności wyższej od 0 na obrazie uzyskanym z detekcji konturowej,
        następnie przeszukuje otoczenie tego piksela w obrazie segemntowanym na podstawie informacyjności.
        Wybrany zostaje obszar o największej gęstości pikseli, następnie obszar ten jest powiększany, dopóki w jego oteczeniu
        są piksele o wartości >0
        :param information_segmented_im:
        :param edge_segmented_image:
        :return:
        """
        szer = len(information_segmented_im[0])
        wys = len(information_segmented_im)

        window_width = int(szer / 40)
        window_height = int(wys / 40)

        im_out = information_segmented_im.copy()
        highest_mean = 0
        obj_x = 0
        obj_y = 0

        """Pierwszy etap - wyszukanie miejsca o największej średniej wartości pikseli"""
        for y in range(0, wys):
            for x in range(0, szer):
                if edge_segmented_image[y][x] > 0 and information_segmented_im[y][x] > 0:
                    mean = 0
                    num = 0
                    for yw in range(0, window_height):
                        for xw in range(0, window_width):
                            try:
                                mean += information_segmented_im[y + yw][x + xw]
                                num += 1
                            except:
                                mean += 0
                    mean = mean / num
                    if mean > highest_mean:
                        highest_mean = mean
                        obj_x = x
                        obj_y = y

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
                            sum[0] += information_segmented_im[obj_y + yw][obj_x + xw]
                            num[0] += 1

                        if ((xw == window_width - 1) and (0 <= yw < window_height)) or (
                                (yw == window_height - 1) and (0 <= xw < window_width)):
                            sum[1] += information_segmented_im[obj_y + yw][obj_x + xw]
                            num[1] += 1
                    except:
                        still_search = False

            for i in range(0, len(sum)):
                if sum[i] != 0 and num[i] != 0:
                    means[i] = sum[i] / num[i]
                else:
                    means[i] = 0

            if means[0] > 0:
                obj_x -= 1
                window_width += 1
                obj_y -= 1
                window_height += 1
                still_search = True
            if means[1] > 0:
                window_width += 1
                window_height += 1
                still_search = True

        # usuwanie pikseli poza okienkiem
        for y in range(0, wys):
            for x in range(0, szer):
                if not ((obj_y - window_height <= y < obj_y + window_height) and (
                        obj_x - window_width <= x < obj_x + window_width)):
                    im_out[y][x] = 0

                """ kod do obrysowywania okienka, należy usunąć przed testowaniem

                if (x == obj_x) and (obj_y <= y < obj_y+window_height):
                    im_out[y][x] = 255
                if (x == obj_x + window_width - 1) and (obj_y <= y < obj_y+window_height):
                    im_out[y][x] = 255
                if (y == obj_y) and (obj_x <= x < obj_x + window_width):
                    im_out[y][x] = 255
                if (y == obj_y+window_height - 1) and (obj_x <= x < obj_x+window_width):
                    im_out[y][x] = 255
                """
        return im_out

    def __search_for_multiple_objects(self, information_segmented_im, edge_segmented_image):
        """
        Test drive
        :param information_segmented_im:
        :param edge_segmented_image:
        :return:
        """
        json_file = []
        information_segmented_im_copy = information_segmented_im.copy()
        im, highest_mean, coords, obj_candidates = self.__search_for_object_more_parameters(information_segmented_im,
                                                                                            edge_segmented_image)
        im_out = im.copy()
        mean_obj_den = self.__mean_object_density(obj_candidates)

        obj_num = 1
        while True:
            information_segmented_im_copy = self.__image_xor(information_segmented_im_copy, mask=im)
            im, mean, _, _ = self.__search_for_object_more_parameters(information_segmented_im_copy,
                                                                      edge_segmented_image)
            json_file.append(self.__data_to_json)
            if mean < mean_obj_den:
                break
            else:
                im_out = self.__image_or(im_out, im)
        return im_out

    @staticmethod
    def __search_for_object_more_parameters(information_segmented_im, edge_segmented_image):
        """
        Metoda do wyszukiwania obiektu na obrazie.
        Działanie: metoda sprawdza położenie pikseli o intensywności wyższej od 0 na obrazie uzyskanym z detekcji konturowej,
        następnie przeszukuje otoczenie tego piksela w obrazie segemntowanym na podstawie informacyjności.
        Wybrany zostaje obszar o największej gęstości pikseli, następnie obszar ten jest powiększany, dopóki w jego oteczeniu
        są piksele o wartości >0
        :param information_segmented_im:
        :param edge_segmented_image:
        :return:
        """
        szer = len(information_segmented_im[0])
        wys = len(information_segmented_im)

        window_width = int(szer / 40)
        window_height = int(wys / 40)

        im_out = information_segmented_im.copy()
        highest_mean = 0
        obj_x = 0
        obj_y = 0
        obj_candidates = {}
        obj_num = 1

        """Pierwszy etap - wyszukanie miejsca o największej średniej wartości pikseli"""
        for y in range(0, wys):
            for x in range(0, szer):
                if edge_segmented_image[y][x] > 0 and information_segmented_im[y][x] > 0:
                    mean = 0
                    num = 0
                    for yw in range(0, window_height):
                        for xw in range(0, window_width):
                            try:
                                mean += information_segmented_im[y + yw][x + xw]
                                num += 1
                            except:
                                mean += 0
                    mean = mean / num
                    obj_candidates[obj_num] = {'x': x, 'y': y, 'mean': mean}
                    obj_num += 1
                    if mean > highest_mean:
                        highest_mean = mean
                        obj_x = x
                        obj_y = y

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
                            sum[0] += information_segmented_im[obj_y + yw][obj_x + xw]
                            num[0] += 1

                        if ((xw == window_width - 1) and (0 <= yw < window_height)) or (
                                (yw == window_height - 1) and (0 <= xw < window_width)):
                            sum[1] += information_segmented_im[obj_y + yw][obj_x + xw]
                            num[1] += 1
                    except:
                        still_search = False

            for i in range(0, len(sum)):
                if sum[i] != 0 and num[i] != 0:
                    means[i] = sum[i] / num[i]
                else:
                    means[i] = 0

            if means[0] > 0:
                obj_x -= 1
                window_width += 1
                obj_y -= 1
                window_height += 1
                still_search = True
            if means[1] > 0:
                window_width += 1
                window_height += 1
                still_search = True

        coords = {'x': obj_x, 'y': obj_y, 'window_width': window_width, 'window_height': window_height}
        # usuwanie pikseli poza okieniem
        for y in range(0, wys):
            for x in range(0, szer):
                if not ((obj_y - window_height <= y < obj_y + window_height) and (
                        obj_x - window_width <= x < obj_x + window_width)):
                    im_out[y][x] = 0
        return im_out, highest_mean, coords, obj_candidates

    @staticmethod
    def __image_xor(image, mask):
        """
        Z image zostanie wymazane wszystko co na masce ma wartość ponad 0
        :param image:
        :param mask:
        :return:
        """
        szer = len(image[0])
        wys = len(image)
        im_out = image.copy()
        for y in range(0, wys):
            for x in range(0, szer):
                if image[y][x] > 0 and mask[y][x] > 0:
                    im_out[y][x] = 0
        return im_out

    @staticmethod
    def __image_or(im1, im2):
        szer = len(im1[0])
        wys = len(im1)
        im_out = im1.copy()
        for y in range(0, wys):
            for x in range(0, szer):
                if im2[y][x] > 0:
                    im_out[y][x] = im2[y][x]
        return im_out

    @staticmethod
    def __mean_object_density(obj_candidates):
        means = []
        for i in range(1, len(obj_candidates) + 1):
            means.append(obj_candidates[i]['mean'])
        return stat.mean(means)

    def __data_to_json(self):
        return {
            "entropy_of_image": self.__entropy_of_image,
            "entropy_of_segmented_image": self.__entropy_of_segmented_image,
            "mean": self.__mean_pixel_value,
            "isValid": self.__isValid,
            "isObjectDetected": self.__is_object_detected,
            "horizontal_angle_of_view": self.__horizontal_angle_dist_from_center,
            "vertical_angle_of_view": self.__vertical_angle_dist_from_center,
            "distance_to_object": self.__distance_to_object,
            "histogram": self.__histogram,
        }

    def setup_for_geo_loc_rot_calculation(self, camera):
        self.__object_geo_loc_calculator.setup(camera)

    def calculate_object_angle_position(self, img, log):
        if log is not None:
            self.__object_geo_loc_calculator.add_img(img, log)
            horizontal_angle_dist_from_center, vertical_angle_dist_from_center = self.__object_geo_loc_calculator.calculate_angle_from_obj_to_camera_center()
            return horizontal_angle_dist_from_center, vertical_angle_dist_from_center
        return None

    def image_entropy_analysis(self, log_file):
        self.__set_all_to_zero()

        if self.__is_img_vignetted(self.img):
            self.img = self.__img_vignetting_correction(self.img)

        self.__check_histogram()
        if not self.__isValid:
            self.__mean_pixel_value, _, self.__std_dev, self.__entropy_of_image = \
                self.__statistical_parameters_calculator.calculate_all(self.img)
            return self.__data_to_json()

        self.__mean_pixel_value, _, _, self.__entropy_of_image = self.__statistical_parameters_calculator.calculate_all(
            self.img)

        """img_segmented_edge = self.__segment_by_contour(self.img, 4)

        if img_segmented_edge is None:
            print("Contour not closed, no object detected on image")
            return self.__data_to_json()"""

        img_segmented_edge = self.__segment_by_contour(self.img, sigma=2)

        if img_segmented_edge is None:
            return self.__data_to_json()

        self.__edge_segmentation_controller.set_img(img_segmented_edge)

        if not self.__edge_segmentation_controller.check_if_contour_exist():
            print("No contour, no object detected on image")
            return self.__data_to_json()

        if not self.__edge_segmentation_controller.check_if_contour_is_closed():
            print("Contour not closed, no object detected on image")
            return self.__data_to_json()

        img_segmented_information = self.__information_threshold_segmentation(std='on')

        if self.__fill_factor > 0.2:
            self.img = self.__img_noise_outside_centre_deleting(self.img)
            img_segmented_information = self.__information_threshold_segmentation(std='on')

        if self.__fill_factor <= 0.1:
            self.img = self.__search_for_object(img_segmented_information, img_segmented_edge)

            _, _, _, self.__entropy_of_segmented_image = self.__statistical_parameters_calculator.calculate_all(
                self.img)

            if self.calculate_object_angle_position(self.img, log_file):
                self.__horizontal_angle_dist_from_center, self.__vertical_angle_dist_from_center = \
                    self.calculate_object_angle_position(self.img, log_file)

            if self.__horizontal_angle_dist_from_center is None or self.__vertical_angle_dist_from_center is None:
                self.__is_object_detected = False
                return self.__data_to_json()

            self.__distance_to_object = self.__calculate_distance_to_object(log_file)

            if self.__is_object_too_big(5):
                self.__is_object_detected = False
                self.__distance_to_object = None
                return self.__data_to_json()

            self.__is_object_detected = True
            self.__histogram = self.__calculate_histogram_to_query(self.img)

        else:
            self.__isValid = False
        return self.__data_to_json()

    def image_entropy_analysis_for_testing(self, log_file):
        """image_entropy_analysis służące do testowamia nowych rozwiązań, podczas pracy metoda pokazuej kolejne
        wyniki przetwarzania obrazu i informuje o wykonywanym zadaniu"""

        """Niezbędne do sprawdzenia całości funkcjonalności programu"""
        self.add_histogram_filtering_data(255, 255)
        """________________________________________"""

        print("Checking if img is vignetted...")
        if self.__is_img_vignetted(self.img):
            print("Img is vignetted, vignetting correction initiated...", end="")
            self.img = self.__img_vignetting_correction(self.img)
            print("Done")

        print("Histogram check started...", end="")
        self.__check_histogram()
        self.show_image()
        if not self.__isValid:
            self.__mean_pixel_value, _, self.__std_dev, self.__entropy_of_image = \
                self.__statistical_parameters_calculator.calculate_all(self.img)
            print("image not valid")
            return self.__data_to_json()

        img_copy = self.img.copy()
        print("DONE - image valid")
        print("Calculating preprocessed image statistical parameters...", end="")
        self.__mean_pixel_value, _, _, self.__entropy_of_image = self.__statistical_parameters_calculator.calculate_all(
            self.img)
        print("DONE")

        print("Segmenting by contour...", end="")
        img_segmented_edge = self.__segment_by_contour(self.img, sigma=2)
        self.show_image_static(img_segmented_edge)
        print("DONE")

        print("First check of edge segmentation - if contour was detected at all...", end="")
        self.__edge_segmentation_controller.set_img(img_segmented_edge)
        if not self.__edge_segmentation_controller.check_if_contour_exist():
            print("no object detected on image")
            return self.__data_to_json()
        print("DONE")

        print("Second check of edge segmentation - if contour is closed...", end="")
        if not self.__edge_segmentation_controller.check_if_contour_is_closed():
            print("No object detected on image")
            return self.__data_to_json()
        print("contour closed")

        print("Segmenting by information...", end="")
        img_segmented_information = self.__information_threshold_segmentation(std='on')
        self.show_image_static(img_segmented_information)
        print("DONE")

        """Próba naprawienia obrazu - usunięcie wszystkich pikseli poza zanjdującymi się w centrum obrazu"""
        if self.__fill_factor > 0.2:
            print("Segmenting by information correction - deleting pixels outside of img centre...", end="")
            self.img = self.__img_noise_outside_centre_deleting(self.img)
            img_segmented_information = self.__information_threshold_segmentation(std='on')
            self.show_image_static(img_segmented_information)
        print("DONE")

        if self.__fill_factor <= 0.1:
            print("Searching for object...", end="")
            self.img = self.__search_for_object(img_segmented_information, img_segmented_edge)
            self.show_image()
            print("DONE")

            _, _, _, self.__entropy_of_segmented_image = self.__statistical_parameters_calculator.calculate_all(
                self.img)

            print("Calculating object position on image...", end="")
            if self.calculate_object_angle_position(self.img, log_file):
                self.__horizontal_angle_dist_from_center, self.__vertical_angle_dist_from_center = \
                    self.calculate_object_angle_position(self.img, log_file)
            print("DONE")

            print("Calculating distance to object on image...", end="")
            self.__calculate_distance_to_object(log_file)
            print('DONE')

            print('Checking if object is no too big...', end="")
            if self.__is_object_too_big(5):
                self.__isValid = False
                print('DONE - object too big')
                return self.__data_to_json()
            print('DONE')

            print('Setting object detection flag as TRUE...', end="")
            self.__is_object_detected = True
            print('DONE')

        else:
            self.__isValid = False
        return self.__data_to_json()

    def __set_all_to_zero(self):
        self.__is_object_detected = False
        self.__isValid = False
        self.__histogram = None
        self.__distance_to_object = None

    def __calculate_histogram_to_query(self, im):
        if self.__isValid and self.__is_object_detected:
            _, histogram = StatisticsParameters.image_histogram_with_offset(im=im, normalize='on', grayscale_offset=1)
            out = []
            for num in histogram:
                out.append(num)
            return {'data': out}
        return None

    @staticmethod
    def __calculate_distance_to_object(log):
        if log is not None:
            print("Distance:", np.abs(float(log['barometric_height']) / (np.cos(float(log['pitch']) * np.pi / 180))))
            return np.abs(float(log['barometric_height']) / (np.cos(float(log['pitch']) * np.pi / 180)))
        return None

    def __is_object_too_big(self, max_object_dim):
        try:
            img_horizontal_dim_in_meters = 2 * np.tan((
                                                                  np.pi / 180) * 0.5 * self.__object_geo_loc_calculator.get_camera_horizontal_fov()) * self.__distance_to_object
            img_vertical_dim_in_meters = 2 * np.tan((
                                                                np.pi / 180) * 0.5 * self.__object_geo_loc_calculator.get_camera_vertical_fov()) * self.__distance_to_object
        except TypeError:
            return False

        acceptable_fill_factor = max_object_dim ** 2 / (img_horizontal_dim_in_meters * img_vertical_dim_in_meters)
        return acceptable_fill_factor < self.__fill_factor

    def __check_histogram(self):
        self.__isValid = False
        grayscale, grayscale_prob = self.__statistical_parameters_calculator.image_histogram(self.img, 'on')
        mean_pixel_value = self.__statistical_parameters_calculator.mean_from_histogram(grayscale, grayscale_prob)
        if mean_pixel_value < self.mean_from_db + self.std_dev_from_db:
            self.__isValid = True

    def __is_img_vignetted(self, img):
        self.__image_quality_controller.add_image(img)
        if self.__image_quality_controller.is_image_vignetted():
            return True
        return False

    def __img_validation_check(self, img):
        self.__check_histogram()
        if not self.__isValid:
            self.__mean_pixel_value, _, self.__std_dev, self.__entropy_of_image = self.__statistical_parameters_calculator.calculate_all(
                self.img)
            print("Histogram check ended, image not valid, trying to remove vignetting")
            self.__image_quality_controller.add_image(self.img)
            self.__image_quality_controller.vignetting_correction(0)
            self.img = self.__image_quality_controller.get_image()
            return self.__data_to_json()

    def __img_vignetting_correction(self, img):
        self.__image_quality_controller.add_image(img)
        self.__image_quality_controller.vignetting_correction(0)
        return self.__image_quality_controller.get_image()

    def __img_noise_outside_centre_deleting(self, img):
        self.__image_quality_controller.add_image(img)
        self.__image_quality_controller.noise_outside_center_reduction()
        return self.__image_quality_controller.get_image()

    def __calculate_object_angle_position_and_distance(self, img, log):
        horizontal_angle_dist_from_center, vertical_angle_dist_from_center = \
            self.calculate_object_angle_position(img, log)
        distance = self.__calculate_distance_to_object(log)
        return horizontal_angle_dist_from_center, vertical_angle_dist_from_center, distance

    def image_entropy_analysis_all_objects(self):
        self.__check_histogram()
        if not self.__isValid:
            self.__mean_pixel_value, _, self.__std_dev, self.__entropy_of_image = self.__statistical_parameters_calculator.calculate_all(
                self.img)
            return self.__data_to_json()
        self.__mean_pixel_value, _, _, _ = self.__statistical_parameters_calculator.calculate_all(self.img)
        img_segmented_edge = self.__contour_segmentation('canny')
        img_segmented_information = self.__information_threshold_segmentation()
        self.img = self.__search_for_multiple_objects(img_segmented_information, img_segmented_edge)
        return self.__data_to_json()

    def show_image(self):
        plt.figure()
        plt.imshow(self.img, cmap=gray())
        plt.show()

    @staticmethod
    def show_image_static(img):
        plt.figure()
        plt.imshow(img, cmap=gray())
        plt.show()

    def get_image(self):
        return self.img


class StatisticsParameters:
    """
    Klasa służąca do oblciznia parametrów statystycznych obrazów za pomocą metod statycznych.
    """

    @staticmethod
    def image_histogram(im, normalize="off"):
        """
        Funkcja służąca do obliczania histogramu z obrazu
        :param normalize:
        :param im:
        :return:
        """
        # im = image_type_validation(im)
        szer = len(im[0])
        wys = len(im)
        grayscale = []  # wektor skali szarości
        for i in range(0, 256):
            grayscale.append(i)
        gray_shade_prob = np.zeros(len(grayscale))  # wektor prawdopodobieństw odcieni szarości
        for y in range(0, wys):
            for x in range(0, szer):
                gray_shade_prob[im[y][x]] += 1
        num = np.sum(gray_shade_prob)  # Ilosc wszystkich pikseli

        # normalizacja
        if normalize == "on":
            for i in range(0, len(gray_shade_prob)):
                gray_shade_prob[i] = gray_shade_prob[i] / num
        return grayscale, gray_shade_prob

    @staticmethod
    def information_gain_between_histograms(original_img_histogram, processed_img_histogram):
        information_gain = 0
        for i in range(0, len(processed_img_histogram)):
            if processed_img_histogram[i] * original_img_histogram[i] > 0:
                information_gain += original_img_histogram[i] * np.log2(
                    original_img_histogram[i] / processed_img_histogram[i])
        return information_gain

    @staticmethod
    def mean_from_histogram(grayscale, gray_shade_prob):
        mean = 0
        for i in range(0, len(grayscale)):
            mean += grayscale[i] * gray_shade_prob[i]
        return mean

    @staticmethod
    def variance_from_histogram(grayscale, gray_shade_prob, mean_value):
        variance = 0
        for i in range(0, len(grayscale)):
            variance += ((grayscale[i] - mean_value) ** 2) * gray_shade_prob[i]
        return variance

    @staticmethod
    def std_dev_from_histogram(variance):
        return sqrt(variance)

    @staticmethod
    def information_entropy(im):
        """
        Metoda obliczająca entropię informacji na obrazie
        :param im:
        :return:
        """
        # Histogram - dyskretny rozkład prawdopodobieństwa
        grayscale, gray_shade_prob = StatisticsParameters.image_histogram(im, "on")

        I_n = []  # informacja zawarta w pikselu

        # Entropia
        H_n = []  # entropia od n
        for p in gray_shade_prob:
            if p == 0:
                I = 0
            else:
                I = -np.log2(p)
            H = p * I
            H_n.append(H)
            I_n.append(I)
        H = np.sum(H_n)  # wartosc entropii
        return H, H_n, I_n

    @staticmethod
    def image_histogram_with_offset(im, normalize="off", grayscale_offset=0):
        """
        Funkcja służąca do obliczania histogramu z obrazu
        :param im:
        :return:
        """
        # im = image_type_validation(im)
        szer = len(im[0])
        wys = len(im)
        grayscale = []  # wektor skali szarości
        for i in range(0, 256):
            grayscale.append(i)
        gray_shade_prob = np.zeros(len(grayscale))  # wektor prawdopodobieństw odcieni szarości

        for y in range(0, wys):
            for x in range(0, szer):
                if im[y][x] > grayscale_offset:
                    gray_shade_prob[im[y][x]] += 1
        num = np.sum(gray_shade_prob)  # Ilosc wszystkich pikseli

        for i in range(0, grayscale_offset):
            gray_shade_prob[i] = 0
        # normalizacja
        if normalize == "on":
            for i in range(0, len(gray_shade_prob)):
                gray_shade_prob[i] = gray_shade_prob[i] / num

        return grayscale, gray_shade_prob

    @staticmethod
    def calculate_all(im):
        grayscale, gray_shade_prob = StatisticsParameters.image_histogram(im, "on")
        mean = StatisticsParameters.mean_from_histogram(grayscale, gray_shade_prob)
        var = StatisticsParameters.variance_from_histogram(grayscale, gray_shade_prob, mean)
        std_dev = StatisticsParameters.std_dev_from_histogram(var)
        entropy, entropy_per_pixel_val, information_per_pixel_val = StatisticsParameters.information_entropy(im)
        return mean, var, std_dev, entropy


class ImageQualityController:
    def __init__(self):
        self.__img = None
        self.__szer = 0
        self.__wys = 0
        self.__fill_factor = 0

    def add_fill_factor(self, fill_factor):
        self.__fill_factor = fill_factor

    def add_image(self, img):
        self.__img = img
        self.__szer = len(self.__img[0])
        self.__wys = len(self.__img)

    def get_image(self):
        return self.__img

    def is_image_vignetted(self):

        nrows, ncols = self.__img.shape
        row, col = np.ogrid[:nrows, :ncols]
        cnt_row, cnt_col = nrows / 2, ncols / 2
        outer_disk_mask = ((row - cnt_row) ** 2 + (col - cnt_col) ** 2 > (nrows / 2) ** 2)

        outer_disk_pixels = []
        inner_disk_pixels = []

        for y in range(0, self.__wys):
            for x in range(0, self.__szer):
                if outer_disk_mask[y][x]:
                    outer_disk_pixels.append(self.__img[y][x])
                else:
                    inner_disk_pixels.append(self.__img[y][x])

        if mean(outer_disk_pixels) > mean(inner_disk_pixels) + 0.2 * mean(outer_disk_pixels):
            return True
        return False

    def vignetting_correction(self, limit_offset=0):

        rows, cols = self.__img.shape[:2]

        # generating vignette mask using Gaussian
        # generating resultant_kernel matrix
        resultant_kernel = self.gkern(cols, rows)

        # creating mask and normalising by using np.linalg
        mask = 255 * resultant_kernel / np.linalg.norm(resultant_kernel)
        self.__img = uint8(self.__img * mask)

    def noise_outside_center_reduction(self):
        self.__disk_mask()

    def __disk_mask(self):
        nrows, ncols = self.__img.shape
        row, col = np.ogrid[:nrows, :ncols]
        cnt_row, cnt_col = nrows / 2, ncols / 2
        outer_disk_mask = ((row - cnt_row) ** 2 + (col - cnt_col) ** 2 > (nrows / 2) ** 2)
        for y in range(0, self.__wys):
            for x in range(0, self.__szer):
                if outer_disk_mask[y][x]:
                    self.__img[y][x] = 0

    @staticmethod
    def gkern(cols, rows, nsig=1):
        """Returns a 2D Gaussian kernel."""

        x = np.linspace(-nsig, nsig, cols + 1)
        kern1d_x = np.diff(norm.cdf(x))

        y = np.linspace(-nsig, nsig, rows + 1)
        kern1d_y = np.diff(norm.cdf(y))

        kern2d = np.outer(kern1d_y, kern1d_x)
        return kern2d / kern2d.sum()


class ObjectDetectionTester:
    """
    Klasa pozwalająca na okreslenie, czy kontur obiektu jest zamknięty
    """

    def __init__(self):
        self.__img = None
        self.__szer = 0
        self.__wys = 0

    def set_img(self, contour_segmented_img):
        self.__img = contour_segmented_img
        self.__img = closing(self.__img)
        self.__szer = len(self.__img[0])
        self.__wys = len(self.__img)

    def get_img(self):
        return self.__img

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

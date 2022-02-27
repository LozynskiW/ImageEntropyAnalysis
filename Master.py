from InformationGainAnalysis.DataStorage import DataBase
from InformationGainAnalysis.DataStorage import LocalDataStorage
from InformationGainAnalysis.InformationEntropyAnalysis import ImageInformationAnalysis
from InformationGainAnalysis.DBdataProcessor import DBdataProcessor
from InformationGainAnalysis.HistogramAnalyser import HistogramAnalyser
from statistics import mean
from math import sqrt
import numpy as np


class Master:
    """
    Klasa służąca do obsługiwania klas LocalDataStoraga, DataBase i ImageEntropyAnalysis, by zapewnić współpracę
    lokalnej maszynie służącej do przetwarzania danych i bazie danych. Dodatkowo ma umozliwiać wysyłanie zapytań do bazy
    danych
    """

    def __init__(self):
        self.__data_base = DataBase()
        self.__local_storage = LocalDataStorage()
        self.__image_processing_blackbox = ImageInformationAnalysis()
        self.__db_data_processor = DBdataProcessor()
        self.__histogram_analyser = HistogramAnalyser()
        self.__query_assistance = DBQueryAssistance()
        """Zależności"""
        self.__local_storage.change_information_processing_blackbox(self.__image_processing_blackbox)
        """Dane o lokalizacji plików"""
        self.__object = None
        """Zmienne do przechowywania danych dynamicznych"""
        self.__data_from_db = []

    def check_if_already_in_db(self, object, dataset, image):
        try:
            return len(self.__data_base.find_specific(self.__form_query_to_find_image(object, dataset, image))) > 0
        except AttributeError:
            return False

    def __calculate_mean_and_std_from_luminosity(self):
        """
        Metoda służąca do oblicznia wartości średniej luminancji obrazów liczona ze wszysystkich obrazów z danego zbioru
        Następnie wartość średnia wykorzystywana jest do obliczenia odchylenia standardowego
        :return:
        """
        try:
            query = self.__query_assistance.form_query_to_get_single_dataset(
                object=self.__object,
                dataset=self.__local_storage.get_dataset(),
                validation_type=None
            )
            all_dataset = self.__data_base.find_specific(query)

        except AttributeError:
            all_dataset = {"mean": 0}

        if not all_dataset:
            return 0, 0

        mean_luminosity = mean(map(lambda reg: float(reg['mean']), all_dataset))
        var_luminosity = map(lambda reg: (float(reg["mean"]) - float(mean_luminosity)) ** 2, all_dataset)
        std_dev_luminosity = sum(map(lambda var: sqrt(var), var_luminosity)) * (1 / len(all_dataset))
        return mean_luminosity, std_dev_luminosity

    def delete_from_db(self, query):
        self.__data_base.delete_in_db(query)

    @staticmethod
    def __form_query_to_find_image(object, dataset, image):
        return {"object": object, "dataset": dataset, "file": image}

    @staticmethod
    def __form_query_to_update(isValid, isObjDetected, entropy, horizontal_angle, vertical_angle, distance_to_object,
                               histogram):
        return {"$set": {"isValid": isValid,
                         "isObjectDetected": isObjDetected,
                         "entropy_of_segmented_image": entropy,
                         "horizontal_angle_of_view": horizontal_angle,
                         "vertical_angle_of_view": vertical_angle,
                         "distance_to_object": distance_to_object,
                         "histogram": histogram}}

    def choose_data(self, object, folder):
        """
        Method used to select main folder containing one, specific dataset
        Folder should be in format:
            bear (object)
            -> name of dataset (folder)
            -> name of dataset (folder)
        :param object: name of main folder containing datasets for one object (for example bear or donkey or tank)
        :param folder: name of folder containing one dataset for object
        :return:
        """
        self.__object = object
        self.__local_storage.choose_data(self.__object, folder)
        self.__data_base.choose_collection(self.__object)

    def choose_object(self, object):
        """
        Method used to select main folder containing multiple datasets, all in different folders
        Folder should be in format:
            bear (object)
            -> name of dataset (folder)
            -> name of dataset (folder)
        :param object: name of main folder containing datasets for one object (for example bear or donkey or tank)
        :return:
        """
        self.__object = object
        self.__local_storage.set_object(object)
        self.__data_base.choose_collection(self.__object)

    def choose_folder(self, folder):
        self.__local_storage.choose_data(self.__object, folder)
        self.__data_base.choose_collection(self.__object)

    def set_main_folder(self, folder_path):
        self.__local_storage.change_main_folder(folder_path)

    def change_information_processing_blackbox(self, information_processing_blackbox):
        self.__image_processing_blackbox = information_processing_blackbox

    def set_data_from_db(self, data_from_db):
        self.__data_from_db = data_from_db

    def __data_to_json(self, image_file, statistical_parameters, data_from_log):
        """Metoda do prekształcania danych do postaci możliwej do umieszczenia w baze danych - format json -
        słownik w pythonie"""

        horizontal_angle_of_view = statistical_parameters['horizontal_angle_of_view']
        if horizontal_angle_of_view is not None:
            horizontal_angle_of_view = float(horizontal_angle_of_view)

        vertical_angle_of_view = statistical_parameters['vertical_angle_of_view']
        if vertical_angle_of_view is not None:
            vertical_angle_of_view = float(vertical_angle_of_view)

        distance_to_object = statistical_parameters['distance_to_object']
        if distance_to_object is not None:
            distance_to_object = float(distance_to_object)

        return {
            "object": str(self.__object),
            "dataset": str(self.__local_storage.get_dataset()),
            "file": str(image_file),
            "isValid": statistical_parameters['isValid'],
            "isObjectDetected": statistical_parameters['isObjectDetected'],
            "entropy_of_image": float(statistical_parameters['entropy_of_image']),
            "entropy_of_segmented_image": float(statistical_parameters['entropy_of_segmented_image']),
            "mean": float(statistical_parameters['mean']),
            "time": data_from_log["time"] if data_from_log is not None else None,
            "longitude": float(data_from_log["longitude"]) if data_from_log is not None else None,
            "latitude": float(data_from_log["latitude"]) if data_from_log is not None else None,
            "gps_height": float(data_from_log["gps_height"]) if data_from_log is not None else None,
            "barometric_height": float(data_from_log["barometric_height"]) if data_from_log is not None else None,
            "pitch": float(data_from_log["pitch"]) if data_from_log is not None else None,
            "roll": float(data_from_log["roll"]) if data_from_log is not None else None,
            "yaw": float(data_from_log["yaw"]) if data_from_log is not None else None,
            "gps_speed": float(data_from_log["gps_speed"]) if data_from_log is not None else None,
            "gps_course": float(data_from_log["gps_course"]) if data_from_log is not None else None,
            "horizontal_angle_of_view": horizontal_angle_of_view,
            "vertical_angle_of_view": vertical_angle_of_view,
            "distance_to_object": distance_to_object,
            "histogram": statistical_parameters['histogram']
        }

    @staticmethod
    def __get_data_from_log(log, num):
        if log[10][num] is None:
            raise AttributeError
        try:
            return {
                "time": log[0][num],
                "longitude": float(log[1][num]),
                "latitude": float(log[2][num]),
                "gps_height": float(log[3][num]),
                "barometric_height": float(log[4][num]),
                "pitch": float(log[5][num]),
                "roll": float(log[6][num]),
                "yaw": float(log[7][num]),
                "gps_speed": float(log[8][num]),
                "gps_course": float(log[9][num])
            }
        except ValueError:
            return None

    def analyze_dataset(self, mode='void', dataset_validation=True, limit=None):
        """
        Metoda służąca do analizowania wskazanego w self.__dataset_path zestawu zdjęć w termowizji pod kątem ich
        informacyjności. Wykorzystana do tego jest klasa ImageEntropyAnalysis.ImageInformationAnalysis. Wynikiem
        działania klasy są parametry statstyczne: średnia wartość piksela, odchylenie std i parametrs isValid
        oznaczający, czy obraz nadaje się do analizy informacyjności.
        W celu przebadania wstępnego bazy danych należy jako parametry mean_pixel_value_from_db, std_of_mean_pixel_value_from_db
        ustawić wartości minimalnie dające po zsumowaniu 255, a w przypadku faktycznej analizy wartości pobrane z bazy
        danych.

        Tryby:
            "void" - pokazuje wyniki analizy określonych w zapytaniu danych dla przekazanych parametrów mean i std_dev
            "create" - analizuje wybrany zbiór i wpisuje rejestry do bazy danych, bez sprawdzenia, czy one już tam
                        nie występują, każdy rejest będzie miał ustawiony parametr isValid na false
            "update" - analizuje wybrany zbiór i nadpisuje znajdujące się już w bazie danych rejestry
            "mixed" - analizuje wybrany zbiór i jeżeli obraz jest w bazie danych to go nadpisuje, jęzeli nie, to
                        go dodaje
            "test" - analiza obrazu z dokładną wizualizacją wyniku działania każdej metody i z komunikatami odnośnie
                    obecnie wykonywanej operacji

        :param limit:
        :param dataset_validation: if True then parameters for statistical selection will be downloaded from db
        :param mode:
        :return:
        """
        try:
            self.__data_base.choose_collection(self.__object)
        except:
            self.__data_base.create_collection(self.__object)

        try:
            dataset, log = self.__local_storage.get_folder_contents_from_log()
        except FileNotFoundError:
            print("No log was found, trying to get folder contents manually")

            try:
                dataset = self.__local_storage.get_folder_contents()
                log = None
            except FileNotFoundError:
                print("No folder was found, try setting other dataset path")
                return None

        if dataset is None or len(dataset) <= 0:
            return None

        if mode == 'create':
            self.__image_processing_blackbox.add_histogram_filtering_data()
        else:
            if dataset_validation:
                mean = float(self.__calculate_mean_and_std_from_luminosity()[0])
                std_def = float(self.__calculate_mean_and_std_from_luminosity()[1])
            else:
                mean = 255
                std_def = 255
            self.__image_processing_blackbox.add_histogram_filtering_data(mean, std_def)

        num = 1
        self.__image_processing_blackbox.setup_for_geo_loc_rot_calculation('')

        for image in dataset:
            print('Current image:', image, 'obj class: ', self.__object, '|', num, '/', len(dataset))
            self.__image_processing_blackbox.add_image_from_path(
                self.__local_storage.get_current_dataset_path() + image)

            if log is not None:
                if self.__get_data_from_log(log, num) is not None:
                    data_from_log = self.__get_data_from_log(log, num)
                else:
                    continue
            else:
                data_from_log = None

            if mode == 'test':
                stat_parameters = self.__image_processing_blackbox.image_entropy_analysis(data_from_log, test_mode=True)
            else:
                stat_parameters = self.__image_processing_blackbox.image_entropy_analysis(data_from_log)
            db_query = self.__data_to_json(image, stat_parameters, data_from_log)
            print(db_query)

            if mode == 'mixed' or mode == 'update':
                if self.check_if_already_in_db(self.__object, self.__local_storage.get_dataset(), image):

                    self.__data_base.update_in_db(
                        self.__form_query_to_find_image(db_query["object"],
                                                        db_query["dataset"],
                                                        db_query["file"]),

                        self.__form_query_to_update(db_query["isValid"],
                                                    db_query["isObjectDetected"],
                                                    db_query["entropy_of_segmented_image"],
                                                    db_query["horizontal_angle_of_view"],
                                                    db_query["vertical_angle_of_view"],
                                                    db_query["distance_to_object"],
                                                    db_query["histogram"]))
                else:
                    if mode == 'mixed':
                        self.__data_base.put_to_db(db_query)

            if mode == 'create':
                if not self.check_if_already_in_db(self.__object, self.__local_storage.get_dataset(), image):
                    self.__data_base.put_to_db(db_query)
                else:
                    print('Image:', image, 'of object class: ', self.__object, 'is already in database')

            if mode == 'create' or mode == 'void' or mode == 'test':
                print(db_query)
            num += 1

            if limit:
                if num >= limit:
                    print("FINISHED")
                    break

    def analyse_histogram_of_all_dataset(self, limit=None):

        for object in self.__data_base.get_collections():
            if object != 'histogramsOfObjects':
                self.__data_base.choose_collection(object)

                distinct_datasets = []
                datasets = self.__data_base.find_specific(self.__query_assistance.form_query_to_get_data(
                    validation_type='detected'))

                for d in datasets:
                    if d['dataset'] not in distinct_datasets:
                        distinct_datasets.append(d['dataset'])

                for d in distinct_datasets:

                    query = self.__query_assistance.form_query_to_get_single_dataset(
                        object=object,
                        dataset=d,
                        validation_type='detected'
                    )
                    self.__data_base.choose_collection(object)
                    dataset = self.__data_base.find_specific(query)
                    self.__histogram_analyser.restart()
                    num = 1
                    for data in dataset:
                        self.__histogram_analyser.add_histogram_from_db(data)

                        num += 1

                        if limit:
                            if num == limit:
                                break

                    self.__histogram_analyser.calculate_mean_histogram()
                    self.__data_base.choose_collection("histogramsOfObjects")

                    histogram_json = {
                        "object": object,
                        "dataset": d,
                        "histogram": self.__histogram_analyser.get_saved_histogram_as_query(),
                    }

                    # self.__histogram_analyser.show_histogram()

                    self.__data_base.delete_if_exist({
                        "object": self.__object,
                        "dataset": d})
                    self.__data_base.put_to_db(histogram_json)

    def match_img_with_pattern(self, img, target_histogram):
        """
        Metoda służąca do porównania obiektu lub histogramu obiektu z wzorcem
        :param img:
        :param img_histogram:
        :return:
        """

        if self.__histogram_analyser.get_patterns() is None or len(self.__histogram_analyser.get_patterns()) < 1:
            self.__download_patterns_from_db()

        if img is not None:
            self.__image_processing_blackbox.add_image(img)
            data = self.__image_processing_blackbox.image_entropy_analysis(None)
            target_histogram = data['histogram']

        if isinstance(target_histogram[0], dict):
            target_histogram = target_histogram[0]['histogram']['data']

        out_max, out_min = self.__histogram_analyser.compare_with_all_patterns(target_histogram=target_histogram)

        print('MAX:', out_max)
        print('MIN:', out_min)

    def __download_patterns_from_db(self):

        self.__data_base.choose_collection('histogramsOfObjects')

        patterns = self.__data_base.find_specific({})

        self.__histogram_analyser.add_patterns_from_db(patterns)

    def analyse_all_datasets_for_single_object(self, mode='mixed', dataset_validation=True,
                                               limit_of_img_per_dataset=500):

        """for folder in self.__local_storage.get_folder_contents():
            self.choose_data(object, folder)
            self.analyze_dataset_with_flight_parameters_from_log_file('create', limit_of_img_per_dataset)"""

        for folder in self.__local_storage.get_folder_contents():
            self.choose_data(self.__object, folder)
            self.analyze_dataset(mode=mode,
                                 dataset_validation=dataset_validation,
                                 limit=limit_of_img_per_dataset)

    def plot(self):
        return Master.Plot(self.__data_from_db, self.__db_data_processor)

    def load_data(self):
        return Master.LoadData(self.__data_base, self.__local_storage, self.__query_assistance, self.__object)

    class LoadData:

        def __init__(self, data_base, local_storage, query_assistance, object):
            self.__local_storage = local_storage
            self.__data_base = data_base
            self.__query_assistance = query_assistance
            self.__object = object

        def all_classes_of_objects_data(self, validation='detected'):

            data_from_db = []

            try:
                classes_of_objects = self.__data_base.list_collections()

                query = self.__query_assistance.form_query_to_get_data(validation_type=validation)

                for coo in classes_of_objects:
                    if coo == 'histogramsOfObjects':
                        continue
                    self.__data_base.choose_collection(coo)
                    temp_data = self.__data_base.find_specific(query)

                    for d in temp_data:
                        data_from_db.append(d)

                return data_from_db

            except RuntimeError:
                return []

        def all_data_for_object_from_db(self, scope='object', validation='full'):

            try:

                if scope == 'dataset' and validation == 'full':
                    return self.__data_base \
                        .find_specific(DBQueryAssistance
                                       .form_query_to_get_whole_dataset_validation_check_object_detected(self.__object,
                                                                                                         self.__local_storage.get_dataset()))
                elif scope == 'object' and validation == 'full':
                    return self.__data_base \
                        .find_specific(DBQueryAssistance
                                       .form_query_to_get_all_datasets(self.__object,
                                                                       validation_type='detected'))
                elif scope == 'object' and validation == 'partial':
                    return self.__data_base \
                        .find_specific(DBQueryAssistance
                                       .form_query_to_get_all_datasets(self.__object,
                                                                       validation_type='validated'))

                elif scope == 'object' and validation == 'none':
                    return self.__data_base \
                        .find_specific(DBQueryAssistance
                                       .form_query_to_get_all_datasets(self.__object))

            except RuntimeError:
                return []

        def specific_data_from_db(self, query, save_in_cache=False):

            try:
                data_from_db = self.__data_base.find_specific(query)
            except RuntimeError:
                return []
            else:
                if save_in_cache:
                    self.__data_from_db = data_from_db

                return data_from_db

    class Plot:

        def __init__(self, data, plotting_processor):
            self.__data = data
            self.__plotting_processor = plotting_processor

        def scatter_plot_3d(self, x=None, y=None, z=None):

            if x is None or y is None or z is None:
                raise ValueError("x and y must be set")

            self.__plotting_processor.get_data_with_respect_to(data=self.__data, ox=x, oy=y)
            self.__plotting_processor(plot_type='scatter', ox_label=x, oy_label=y)

        def scatter_plot(self, x=None, y=None):

            if x is None or y is None:
                raise ValueError("x and y must be set")

            self.__plotting_processor.get_data_with_respect_to(data=self.__data, ox=x, oy=y)
            self.__plotting_processor.plot(plot_type='scatter', ox_label=x, oy_label=y)

        def line_plot(self, x=None, y=None):

            if x is None or y is None:
                raise ValueError("x and y must be set")

            self.__plotting_processor.get_data_with_respect_to(data=self.__data, ox=x, oy=y)
            self.__plotting_processor.plot(plot_type='line', ox_label=x, oy_label=y)

        def bar_plot(self, x=None, y=None):

            if x is None or y is None:
                raise ValueError("x and y must be set")

            self.__plotting_processor.get_data_with_respect_to(data=self.__data, ox=x, oy=y)
            self.__plotting_processor.plot(plot_type='bar', ox_label=x, oy_label=y)

        def save_figures_for_whole_dataset(self, object):

            data_to_plot = ["pitch", "roll", "yaw", "distance_to_object", "barometric_height",
                            "horizontal_angle_of_view",
                            "vertical_angle_of_view", "mean", "entropy_of_image"]

            for data in data_to_plot:
                self.__plotting_processor.plot_whole_dataset(data=self.__data,
                                                             ox=data,
                                                             oy="entropy_of_segmented_image",
                                                             mode="save",
                                                             filename=object)

        def with_respect_to_group_by_dataset(self, x, y, translate_names_to_deg=False):
            self.__plotting_processor.plot_whole_dataset(data=self.__data,
                                                         ox=x,
                                                         oy=y,
                                                         mode="show",
                                                         translate_names_to_deg=translate_names_to_deg)

        def comparing_all_classes_of_objects(self, y):
            self.__plotting_processor.group_and_plot_data_by_object_class(self.__data, oy=y, mean='on')


class DBQueryAssistance:
    @staticmethod
    def form_query_to_find_image(object, dataset, image):
        return {"object": object, "dataset": dataset, "file": image}

    @staticmethod
    def form_query_to_update(isValid, entropy, mean):
        return {"$set": {"isValid": isValid, "entropy_of_segmented_image": entropy, "mean": mean}}

    @staticmethod
    def form_query_to_get_whole_dataset_validation_check(object, dataset, isValid=True):
        return {"object": object, "dataset": dataset, "isValid": isValid}

    @staticmethod
    def form_query_to_get_whole_dataset_validation_check_object_detected(object, dataset, isValid=True):
        return {"object": object, "dataset": dataset, "isValid": isValid, "isObjectDetected": True}

    @staticmethod
    def form_query_to_get_single_dataset(object, dataset, validation_type=None):
        if validation_type is None:
            return {"object": object, "dataset": dataset}
        if validation_type == 'validated':
            return {"object": object, "dataset": dataset, "isValid": True}
        if validation_type == 'detected':
            return {"object": object, "dataset": dataset, "isValid": True, "isObjectDetected": True}

    @staticmethod
    def form_query_to_get_all_datasets(object, validation_type=None):
        if validation_type is None:
            return {"object": object}
        if validation_type == 'validated':
            return {"object": object, "isValid": True}
        if validation_type == 'detected':
            return {"object": object, "isValid": True, "isObjectDetected": True}

    @staticmethod
    def form_query_to_get_validated_and_detected_images(object):
        return {"object": object, "isValid": True, "isObjectDetected": True}

    @staticmethod
    def form_query_to_get_data(validation_type=None):
        if validation_type is None:
            return {}
        if validation_type == 'validated':
            return {"isValid": True}
        if validation_type == 'detected':
            return {"isValid": True, "isObjectDetected": True}

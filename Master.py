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
        self.__object = object
        self.__local_storage.choose_data(self.__object, folder)
        self.__data_base.choose_collection(self.__object)

    def choose_object(self, object):
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

    def load_all_classes_of_objects_data(self, validation='detected'):

        classes_of_objects = self.__data_base.list_collections()

        query = self.__query_assistance.form_query_to_get_data(validation_type=validation)

        for coo in classes_of_objects:
            if coo == 'histogramsOfObjects':
                continue
            self.__data_base.choose_collection(coo)
            temp_data = self.__data_base.find_specific(query)

            for d in temp_data:
                self.__data_from_db.append(d)

    def load_data_from_db(self, scope='dataset', validation='full'):
        self.__data_base.choose_collection(self.__object)
        self.__data_from_db = []

        if scope == 'dataset' and validation == 'full':
            self.__data_from_db = self.__data_base \
                .find_specific(DBQueryAssistance
                               .form_query_to_get_whole_dataset_validation_check_object_detected(self.__object,
                                                                                                 self.__local_storage.get_dataset()))
        elif scope == 'object' and validation == 'full':
            self.__data_from_db = self.__data_base \
                .find_specific(DBQueryAssistance
                               .form_query_to_get_all_datasets(self.__object,
                                                               validation_type='detected'))
        elif scope == 'object' and validation == 'partial':
            self.__data_from_db = self.__data_base \
                .find_specific(DBQueryAssistance
                               .form_query_to_get_all_datasets(self.__object,
                                                               validation_type='validated'))

        elif scope == 'object' and validation == 'none':
            self.__data_from_db = self.__data_base \
                .find_specific(DBQueryAssistance
                               .form_query_to_get_all_datasets(self.__object))

    def get_data_from_db(self, query):
        return self.__data_base.find_specific(query)

    def plot_data_with_respect_to(self, plot_type, ox, oy):
        self.__db_data_processor.get_data_with_respect_to(self.__data_from_db, ox, oy)
        self.__db_data_processor.plot(plot_type, ox, oy)

    def plot_data_with_respect_to_group_by_dataset(self, plot_type, ox, oy):
        self.__db_data_processor.group_data_by_dataset(self.__data_from_db, ox, oy)

    def plot_data_with_respect_to_for_whole_dataset(self, plot_type, ox, oy):
        self.__db_data_processor.get_data_with_respect_to(self.__data_from_db, ox, oy)
        self.__db_data_processor.plot(plot_type, ox, oy)

    def plot_data_comparing_all_classes_of_object(self, oy):
        self.__db_data_processor.group_and_plot_data_by_object_class(self.__data_from_db,
                                                                     oy=oy, mean='on')

    def save_figures_for_whole_dataset(self):
        self.__db_data_processor.plot_whole_dataset(data=self.__data_from_db,
                                                    ox="pitch",
                                                    oy="entropy_of_segmented_image",
                                                    mode="save",
                                                    filename=self.__object)
        self.__db_data_processor.plot_whole_dataset(data=self.__data_from_db,
                                                    ox="roll",
                                                    oy="entropy_of_segmented_image",
                                                    mode="save",
                                                    filename=self.__object)
        self.__db_data_processor.plot_whole_dataset(data=self.__data_from_db,
                                                    ox="yaw",
                                                    oy="entropy_of_segmented_image",
                                                    mode="save",
                                                    filename=self.__object)
        self.__db_data_processor.plot_whole_dataset(data=self.__data_from_db,
                                                    ox="distance_to_object",
                                                    oy="entropy_of_segmented_image",
                                                    mode="save",
                                                    filename=self.__object)
        self.__db_data_processor.plot_whole_dataset(data=self.__data_from_db,
                                                    ox= "barometric_height",
                                                    oy="entropy_of_segmented_image",
                                                    mode="save",
                                                    filename=self.__object)
        self.__db_data_processor.plot_whole_dataset(data=self.__data_from_db,
                                                    ox="horizontal_angle_of_view",
                                                    oy="entropy_of_segmented_image",
                                                    mode="save",
                                                    filename=self.__object)
        self.__db_data_processor.plot_whole_dataset(data=self.__data_from_db,
                                                    ox= "vertical_angle_of_view",
                                                    oy="entropy_of_segmented_image",
                                                    mode="save",
                                                    filename=self.__object)
        self.__db_data_processor.plot_whole_dataset(data=self.__data_from_db,
                                                    ox="mean",
                                                    oy="entropy_of_segmented_image",
                                                    mode="save",
                                                    filename=self.__object)
        self.__db_data_processor.plot_whole_dataset(data=self.__data_from_db,
                                                    ox="entropy_of_image",
                                                    oy="entropy_of_segmented_image",
                                                    mode="save",
                                                    filename=self.__object)

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
            "time": data_from_log["time"],
            "longitude": float(data_from_log["longitude"]),
            "latitude": float(data_from_log["latitude"]),
            "gps_height": float(data_from_log["gps_height"]),
            "barometric_height": float(data_from_log["barometric_height"]),
            "pitch": float(data_from_log["pitch"]),
            "roll": float(data_from_log["roll"]),
            "yaw": float(data_from_log["yaw"]),
            "gps_speed": float(data_from_log["gps_speed"]),
            "gps_course": float(data_from_log["gps_course"]),
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

    def analyze_dataset(self, mode='void'):
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

        :param mode:
        :return:
        """
        try:
            self.__data_base.choose_collection(self.__object)
            dataset = self.__local_storage.get_folder_contents()
        except FileNotFoundError:
            print("No folder was found, try setting other dataset path")
            return None
        else:

            if mode == 'create':
                self.__image_processing_blackbox.add_histogram_filtering_data()
            else:
                mean = self.__calculate_mean_and_std_from_luminosity()[0]
                std_def = self.__calculate_mean_and_std_from_luminosity()[1]
                self.__image_processing_blackbox.add_histogram_filtering_data(mean, std_def)

            for image in dataset:

                self.__image_processing_blackbox.add_image_from_path(
                    self.__local_storage.get_current_dataset_path() + image)
                stat_parameters = self.__image_processing_blackbox.image_entropy_analysis()
                db_query = self.__data_to_json(image, stat_parameters)

                if mode == 'mixed':
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
                        self.__data_base.put_to_db(db_query)

                if mode == 'update':
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
                        print('No image in db')

                if mode == 'create':
                    self.__data_base.put_to_db(db_query)

                if mode == 'void':
                    print(db_query)

    def analyze_dataset_with_flight_parameters_from_log_file(self, mode='void', limit=None):
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

        :param mode:
        :return:
        """
        try:
            self.__data_base.choose_collection(self.__object)
            dataset, log = self.__local_storage.get_folder_contents_from_log()
        except FileNotFoundError:
            print("No folder was found, try setting other dataset path")
            return None
        else:

            if mode == 'create':
                self.__image_processing_blackbox.add_histogram_filtering_data()
            else:
                mean = float(self.__calculate_mean_and_std_from_luminosity()[0])
                std_def = float(self.__calculate_mean_and_std_from_luminosity()[1])
                self.__image_processing_blackbox.add_histogram_filtering_data(mean, std_def)

            num = 1
            self.__image_processing_blackbox.setup_for_geo_loc_rot_calculation('')

            for image in dataset:
                print('Current image:', image, 'obj class: ', self.__object, '|', num, '/', len(dataset))
                self.__image_processing_blackbox.add_image_from_path(
                    self.__local_storage.get_current_dataset_path() + image)

                if self.__get_data_from_log(log, num) is not None:
                    data_from_log = self.__get_data_from_log(log, num)
                else:
                    continue

                if mode == 'test':
                    stat_parameters = self.__image_processing_blackbox.image_entropy_analysis_for_testing(data_from_log)
                else:
                    stat_parameters = self.__image_processing_blackbox.image_entropy_analysis(data_from_log)
                db_query = self.__data_to_json(image, stat_parameters, data_from_log)
                print(db_query)

                if mode == 'mixed':
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
                        self.__data_base.put_to_db(db_query)

                if mode == 'update':
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
                        print('No image in db')

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

                    #self.__histogram_analyser.show_histogram()

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

    def complete_analysis_of_whole_dataset(self, object, limit_of_img_per_dataset):
        self.choose_object(object)

        """for folder in self.__local_storage.get_folder_contents():
            self.choose_data(object, folder)
            self.analyze_dataset_with_flight_parameters_from_log_file('create', limit_of_img_per_dataset)"""

        for folder in self.__local_storage.get_folder_contents():
            self.choose_data(object, folder)
            self.analyze_dataset_with_flight_parameters_from_log_file('mixed', limit_of_img_per_dataset)


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


"""dzik, 2021-02-23T235735"""
"""sarna, 2021-02-04T204006"""

test = Master()
test.set_main_folder('D:/magisterka/antrax')

"""test.choose_data('dzik', '2021-02-23T235735')

test.analyze_dataset_with_flight_parameters_from_log_file(
        mode='mixed',
        limit=20)"""

"""
test.analyse_histogram_of_all_dataset(limit=5)
test.load_data_from_db()
test.plot_data_with_respect_to('scatter', "distance_to_object", "entropy_of_segmented_image")
"""
# test.complete_analysis_of_whole_dataset(object='sarna', mode='mixed', limit_of_img_per_dataset=400)
#test.choose_object('sarna')
# test.choose_data('sarna', '2021-02-04T182803')
# test.analyse_histogram_of_all_dataset()

"""test.choose_object('sarna')
test.load_data_from_db(scope='object',
                       validation='full')

test.plot_data_with_respect_to_group_by_dataset("scatter", "horizontal_angle_of_view", "vertical_angle_of_view")"""
#test.save_figures_for_whole_dataset()

#test.analyse_histogram_of_all_dataset()

test.choose_object('dzik')
dzik1_histogram = test.get_data_from_db({"object": "dzik", "file": "2021 02 23 23 57 56 005.tiff"})
dzik2_histogram = test.get_data_from_db({"object": "dzik", "file": "2021 02 04 23 37 15 249.tif"})
test.choose_object('zajac')
zajac1_histogram = test.get_data_from_db({"object": "zajac", "file": "2021 02 02 20 04 27 501.tif"})
zajac2_histogram = test.get_data_from_db({"object": "zajac", "file": "2021 02 04 05 32 32 226.tif"})
test.choose_object('daniel')
daniel1_histogram = test.get_data_from_db({"object": "daniel", "file": "2021 02 05 00 46 25 807.tif"})
daniel2_histogram = test.get_data_from_db({"object": "daniel", "file": "2021 02 02 20 40 50 798.tif"})
test.choose_object('sarna')
sarna1_histogram = test.get_data_from_db({"object": "sarna", "file": "2021 02 04 18 28 03 883.tif"})
sarna2_histogram = test.get_data_from_db({"object": "sarna", "file": "2021 02 04 23 25 42 075.tif"})

test.match_img_with_pattern(img=None, target_histogram=dzik1_histogram)
test.match_img_with_pattern(img=None, target_histogram=dzik2_histogram)
test.match_img_with_pattern(img=None, target_histogram=zajac1_histogram)
test.match_img_with_pattern(img=None, target_histogram=zajac2_histogram)
test.match_img_with_pattern(img=None, target_histogram=daniel1_histogram)
test.match_img_with_pattern(img=None, target_histogram=daniel2_histogram)
test.match_img_with_pattern(img=None, target_histogram=sarna1_histogram)
test.match_img_with_pattern(img=None, target_histogram=sarna2_histogram)


test.load_all_classes_of_objects_data('detected')
test.plot_data_comparing_all_classes_of_object(oy="distance_to_object")


"""
test.plot_data_with_respect_to_group_by_dataset('scatter',
                                                "time",
                                                "entropy_of_segmented_image")
                                                
test.plot_data_with_respect_to_group_by_dataset('scatter', "pitch", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "roll", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "yaw", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "distance_to_object", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "barometric_height", "entropy_of_segmented_image")


test.plot_data_with_respect_to_group_by_dataset('scatter', "horizontal_angle_of_view", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "vertical_angle_of_view", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "mean", "entropy_of_segmented_image")
test.plot_data_with_respect_to_group_by_dataset('scatter', "entropy_of_image", "entropy_of_segmented_image")"""

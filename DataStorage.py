import pymongo
import os
from InformationGainAnalysis.InformationEntropyAnalysis import ImageInformationAnalysis
import pandas as pd
from skimage import io


class DataBase:
    """
    Klasa służąca do komunikacji z bazą danych:
        - wprowadzania nowych danych C
        - pobierania danych R
        - aktualizacji danych U
    TODO opisać klasę i metody"""

    def __init__(self):
        self.__client = pymongo.MongoClient("mongodb://localhost:27017")
        self.__db_database = self.__client["ThermoVisionEntropyAnalysis"]
        self.__db_collection = None
        self.__input_collection = None

    def choose_collection(self, collection):
        """ Metoda służąca do wybrania kolekcji"""
        self.__db_collection = collection
        collist = self.__db_database.list_collection_names()
        if collection not in collist:
            print('No such collection in db')
            self.__db_collection = collection
        self.__input_collection = self.__db_database[self.__db_collection]

    def create_collection(self, collection_name):
        self.__db_database.create_collection(collection_name)

    def put_to_db(self, json_file):
        """ Metoda służąca do wprowadzania danych do bazy danych"""
        self.__input_collection.insert_one(json_file)

    def update_in_db(self, query, json_file):
        """ Metoda służąca do aktualizowania danych w bazie danych"""
        print('BEFORE:', self.find_specific(query))
        self.__input_collection.update_one(query, json_file)
        print('AFTER:', self.find_specific(query))

    def delete_in_db(self, query):
        """Metoda służąca do usuwania danych z bazy"""
        self.__input_collection.delete_one(query)
        print('DELETED: ', query)

    def list_collections(self):
        """ Metoda służąca do wypisania wszystkich kolekcji z bazy danych"""
        collist = self.__db_database.list_collection_names()
        for col in collist:
            print(col)
        return collist

    def get_collections(self):
        return self.__db_database.list_collection_names()

    def delete_if_exist(self, query):
        """ Metoda służąca do usunięcia rekordu z bazy danych gdy istnieje"""
        data = self.find_specific(query)
        if data:
            self.delete_in_db(query)

    def find_specific(self, query):
        """Metoda służąca do pobrania i zwrócenia danych spełniających warunki podane w zapytaniu"""
        mydoc = self.__input_collection.find(query, {"_id": 0})
        out = []
        for x in mydoc:
            out.append(x)
        return out

    def list_all_passing_query(self, query):
        """Metoda służąca do pobrania i wypisania danych spełniających warunki podane w zapytaniu"""
        mydoc = self.__input_collection.find(query, {"_id": 0})
        for x in mydoc:
            print(x)


class LocalDataStorage:
    """
    Klasa służąca do wybierania zdjęć służących do analizy i analizownaiu ich za pomocą klasy ImageEntropyAnalysis
    Opiera się na wykorzystaniu modułu os. Wszystkie dane muszą znajdować się w folderze data, który musi znajdować się
    w miejscu znajdowania się klasy.
    Struktura plików:
    data - lub wybrany metodą change_dataset_path
        -> dzik
            -> jurata
                -> IM_200.jpg
                -> IM_201.jpg
                -> IM_202.jpg
                -> IM_203.jpg
            -> poligon_wat
            -> cokolwiek innego
        -> daniel
        -> sarna
        -> cokolwiek innego

    Po przeanalizowaniu zdjęcia jego parametry zostają zapisane w bazie danych w kolekcji np dzik w katalogu jurata
    """

    def __init__(self):
        self.__main_folder = 'data'
        self.__object = None
        self.__dataset = None
        self.__dataset_path = None
        self.__information_processing_blackbox = ImageInformationAnalysis()

    def change_information_processing_blackbox(self, information_processing_blackbox):
        self.__information_processing_blackbox = information_processing_blackbox

    def change_main_folder(self, path_to_main):
        self.__main_folder = path_to_main

    @staticmethod
    def show_datasets():
        main_folder = os.listdir('data')
        for folder in main_folder:
            print(folder)
            folder_datasets = os.listdir('data/' + str(folder))
            for dataset in folder_datasets:
                print('\t', dataset)

    def choose_data(self, data_folder, dataset):
        self.__object = data_folder
        self.__dataset = dataset
        self.__dataset_path = self.__main_folder + '/' + self.__object + '/' + self.__dataset + '/'

    def set_object(self, data_folder):
        self.__object = data_folder
        self.__dataset_path = self.__main_folder + '/' + self.__object + '/'

    def set_dataset(self, data_folder):
        self.__dataset = data_folder
        self.__dataset_path = self.__main_folder + '/' + self.__object + '/' + self.__dataset + '/'

    def __data_to_json(self, image_file, statistical_parameters):
        """Metoda do prekształcania danych do postaci możliwej do umieszczenia w baze danych - format json -
        słownik w pythonie"""
        return {
            "object": self.__object,
            "dataset": self.__dataset,
            "file": image_file,
            "isValid": statistical_parameters['isValid'],
            "entropy": statistical_parameters['entropy'],
            "mean": statistical_parameters['mean'],
        }

    def list_folder_contents(self, folder):
        folder = os.listdir(self.__main_folder + '/' + self.__object + '/' + folder + '/')
        print(self.__main_folder + '/' + self.__object + '/' + str(folder) + '/')
        for content in folder:
            print('\t', content)

    def list_dataset_contents(self):
        folder = os.listdir(self.__dataset_path)
        print(self.__dataset_path)
        for content in folder:
            print('\t', content)

    def get_folder_contents(self):
        return os.listdir(self.__dataset_path)

    def get_dataset(self):
        return self.__dataset

    def get_current_dataset_path(self):
        return self.__dataset_path

    def get_folder_contents_from_log(self):
        all_files = self.get_folder_contents()
        for file in all_files:
            if file == 'log.txt':
                log = pd.read_csv(self.__dataset_path + '/' + 'log.txt',
                                  sep="\t",
                                  header=None,
                                  skiprows=1,
                                  error_bad_lines=False)
                file_names = log[10]
                file_names.pop(0)
                return file_names, log
        raise FileNotFoundError('No log.txt file found')

    def open_img_from_path(self, img_file_name):
        return io.imread(self.__dataset_path + img_file_name)

    def open_img_from_full_path(self, object, dataset, img_file_name):
        return io.imread(self.__main_folder + "/" + object + "/" + dataset + "/" + img_file_name)


"""
KOD TESTOWY

test = LocalDataStorage()
test.change_main_folder('D:/magisterka/antrax')
test.choose_data('sarna', '2021-02-04T204006')
print(test.get_folder_contents())
file_names, log = test.get_folder_contents_from_log()
print(log[0][1])
"""
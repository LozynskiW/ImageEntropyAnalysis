import pymongo
import os
from InformationGainAnalysis.InformationEntropyAnalysis import ImageInformationAnalysis
import pandas as pd
from skimage import io


class DataBase:
    """
    Used for communication with data base and CRUD operations execution

    Attributes
    ----------
    __client : pymongo.MongoClient()
        Hardcoded implementation of MongoDB Python API - PyMongo allowing for communication with database server.
        Database is set to localhost
    __db_database : pymongo.MongoClient()[]
        Hardcoded MongoDB Shell set in __client DB to store all collections
    __db_collection : str
        Name of collection to perform CRUD operations on

    Data is going to be saved as follows:
    mongodb://localhost:27017 - hardcoded as pymongo.MongoClient()[], set by __client
        -> ThermoVisionEntropyAnalysis - hardcoded to MongoClient, set by __db_database
            -> deer - collection, set by __db_collection
                -> {} - document, most of the time it is going to be provided by json_file parameter
                -> {} - document
            -> boar
            -> rabbit
            -> (...)
    """

    def __init__(self):
        """
        Parameters
        ----------
        self.__client : pymongo.MongoClient("mongodb://localhost:27017")
           Hardcoded implementation of MongoDB Python API - PyMongo allowing for communication with database server.
           Database is set to localhost
        self.__db_database : pymongo.MongoClient()[]
           Hardcoded MongoDB Shell set in __client DB to store all collections
        self.__db_collection : None
           Name of collection to perform CRUD operations on. By default it is set to None so it is required to set it's
           value by choose_collection()
        """
        self.__client = pymongo.MongoClient("mongodb://localhost:27017")
        self.__db_database = self.__client["ThermoVisionEntropyAnalysis"]
        self.__db_collection = None

    def check_if_collection_exists(self, collection):
        """
        Checks if collection is in currently set __db_database. If it is then method returns True, if not False

        Parameters
        ----------
        collection : str
           Name of collection that is going to be checked for existence

        Raises
        ------

        Returns
        -------
        """

        collection_list = self.__db_database.list_collection_names()

        return collection in collection_list

    def choose_collection(self, collection):
        """
        Checks if collection is in currently set __db_database and if it is there it sets value of __db_collection
        which allows CRUD operations on chosen collection

        Parameters
        ----------
        collection : str
           Name of collection that is going to be set as target for CRUD operations

        Raises
        ------
        AttributeError
           If collection is not found in __db_database

        Returns
        -------
        """

        if not self.check_if_collection_exists(collection):
            raise AttributeError('No such collection in db')

        self.__db_collection = self.__db_database[collection]

    def create_collection(self, collection):
        """
        Checks if collection is in currently set __db_database and if it is NOT there it creates one with name of
        collection parameter

        Parameters
        ----------
        collection : str
           Name of collection that is going to be created

        Raises
        ------
        AttributeError
           If collection is found in __db_database

        Returns
        -------
        """

        if self.check_if_collection_exists(collection):
            raise AttributeError('Collection already in db')

        self.__db_database.create_collection(collection)

    def put_to_db(self, json_file):
        """
        Adds document to database

        Parameters
        ----------
        json_file : dict
           Python dict containing all data that is going to be inserted into database

        Raises
        ------
        ValueError
            If json_file is not dict

        Returns
        -------
        """
        if type(json_file) is not dict:
            raise ValueError("json_file mus be dict")

        try:
            self.__db_collection.insert_one(json_file)
        except:
            print("Error in DataBase.put_to_db")

    def delete_in_db(self, query, multiple_delete=False, verbose_mode=True, delete_all=False):
        """
        Deletes single document from database

        Parameters
        ----------
        query : dict
           Python dict containing all data that is going to be used to find document in database
       multiple_delete : bool
            Variable enabling multiple document deletion by single query. False by default
       verbose_mode : bool
            Enables printing messages after deleting document
        delete_all : bool
            Enables empty query, serves as additional security measure preventing from deleting all documents from
            collection by mistake or error

        Raises
        ------
        ValueError
            If query is empty and delete_all is not True

        Returns
        -------
        """
        if query == {} and delete_all == False:
            raise ValueError("query is empty, as a result all documents are going to be updated")

        if multiple_delete:
            self.__db_collection.delete_many(query)
        else:
            self.__db_collection.delete_one(query)

        if verbose_mode:
            print('DELETED: ', query)

    def update_in_db(self, query, json_file, verbose_mode=True, update_all=False):
        """
        Updates document in database

        Parameters
        ----------
        query : dict
           Python dict containing all data that is going to be used to find document in database
        json_file : dict
           Python dict containing all document data that is going to be updated
        verbose_mode : bool
            Variable setting mode where document before updating and after updating will be printed

        Raises
        ------
        ValueError
            If query is empty
        ValueError
            If json_file is empty

        Returns
        -------
        """

        if query == {}:
            raise ValueError("query is empty, as a result all documents are going to be updated")

        if json_file == {}:
            raise ValueError("json_file is empty, nothing to update")

        if verbose_mode:
            print('BEFORE:', self.find_specific(query))

        if update_all:
            self.__db_collection.update_many(query, json_file)
        else:
            self.__db_collection.update_one(query, json_file)

        if verbose_mode:
            print('AFTER:', self.find_specific(query))

    def find_specific(self, query):
        """
        Returns documents from database based on provided query

        Parameters
        ----------
        query : dict
           Python dict containing all data that is going to be used to find document in database

        Raises
        ------

        Returns
        List of documents passing a query
        """
        documents_list = self.__db_collection.find(query, {"_id": 0})

        out = []

        for x in documents_list:

            out.append(x)

        return out

    def list_collections(self):
        """
        Prints a list of all collections in DB server

        Parameters
        ----------

        Raises
        ------

        Returns
        -------
        """

        collection_list = self.get_collections()

        for col in collection_list:
            print(col)

    def get_collections(self):
        """
        Returns a list of all collections in DB server

        Parameters
        ----------

        Raises
        ------

        Returns
        List of all collections as Python List
        """
        return self.__db_database.list_collection_names()

    def list_all_documents_passing_query(self, query):
        """
        Prints all documents from database passing provided query

        Parameters
        ----------
        query : dict
           Python dict containing all data that is going to be used to find documents in database

        Raises
        ------

        Returns
        """
        documents_list = self.__db_collection.find(query, {"_id": 0})

        for x in documents_list:
            print(x)


class LocalDataStorage:
    """
    Used for selecting and adding images to cache memory so they can be used in image processing classes.
    File structure in main folder should be as following:
    data - main folder set by __main_folder attribute
        -> boar - class of obj set by __object
            -> jurata - dataset containing multiple images, set by __dataset
                -> IM_200.jpg
                -> IM_201.jpg
                -> IM_202.jpg
                -> IM_203.jpg
                -> (...)
            -> poligon_wat - another dataset, that may be accessed just by setting __dataset
        -> deer - another class of obj set by __object, gives access to other datasets
        -> (...)

    Attributes
    ----------
    __main_folder : str
        Main folder where all datasets will be stored. Default value is 'data'
    __object : str
        = None
    __dataset : str
        = None
    __dataset_path : str
        = None
    """

    def __init__(self):
        """
        Parameters
        ----------
        self.__main_folder : str
           Main folder where all image datasets will be stored. Default value is 'data'. Can only be changed via method
        self.__object : pymongo.MongoClient()[]
           Name of object/class of object registered on images that serves as collection name in database and main
           folder containing all datasets for one object
        self.__dataset : None
           Name of single dataset containing images taken from one observation, saved in database as single key for
           json file containing data about image, for example:
           {
            object: "deer",
            dataset: "2021-02-23T235735",
            entropy_of_image 5.952319357195236,
            (...)
            }
        self.__dataset_path : None
            A path to certain image:
            self.__dataset_path = self.__main_folder + '/' + self.__object + '/' + self.__dataset + '/'
        """
        self.__main_folder = 'data'
        self.__object = None
        self.__dataset = None
        self.__dataset_path = None

    def set_main_folder(self, path_to_main):
        """
        Sets value for self.__main_folder allowing to change localization of main folder containing all datasets.
        By default it's value is relative to folder containing DataStorage.py file. In order to change it to some other
        localization it is required to set path_to_main as absolute path.

        Parameters
        ----------
        path_to_main : str
           String containing path to main folder, path can be either absolute or relative

        Raises
        ------
        ValueError
            If path_to_main is a blank string

        Returns
        -------
        """
        if len(path_to_main) <= 0:
            raise ValueError("path_to_main can't be blank")

        self.__main_folder = path_to_main

    @DeprecationWarning
    def choose_data(self, data_folder, dataset):
        self.__object = data_folder
        self.__dataset = dataset
        self.__dataset_path = self.__main_folder + '/' + self.__object + '/' + self.__dataset + '/'

    def set_object(self, data_folder):
        """
        Sets value for self.__data_folder allowing to change object which datasets can then be saved to cache memory

        Parameters
        ----------
        data_folder : str
           String containing path to object - folder containing datasets for single class of objects -
           from __main_folder

        Raises
        ------
        ValueError
            If data_folder is a blank string

        Returns
        -------
        """

        if len(data_folder) <= 0:
            raise ValueError("data_folder can't be blank")

        self.__object = data_folder
        self.__dataset_path = self.__main_folder + '/' + self.__object + '/'

    def set_dataset(self, data_folder):
        """
        Sets value for self.__data_folder allowing to change object which datasets can then be saved to cache memory

        Parameters
        ----------
        data_folder : str
           String containing path to object - folder containing datasets for single class of objects -
           from __main_folder

        Raises
        ------
        ValueError
            If data_folder is a blank string

        Returns
        -------
        """

        if len(data_folder) <= 0:
            raise ValueError("data_folder can't be blank")

        self.__dataset = data_folder
        self.__dataset_path = self.__main_folder + '/' + self.__object + '/' + self.__dataset + '/'

    def list_datasets(self):
        """
        Prints all datasets for all objects within currently chosen self.__main_folder in following format:
        -> boar
            -> dataset1
            -> dataset2
            -> dataset3
        -> deer
            -> dataset1
            -> dataset2
            -> (...)


        Parameters
        ----------

        Raises
        ------

        Returns
        -------
        """

        main_folder = os.listdir(self.__main_folder)

        for folder in main_folder:
            print(folder)
            folder_datasets = os.listdir(self.__main_folder + str(folder))

            for dataset in folder_datasets:
                print('\t', dataset)

    def list_dataset_contents(self, folder):
        """
        Prints all files for one dataset within currently chosen self.__main_folder + '/' + self.__object:
        Chosen object: deer
        -> dataset1
            -> img001.png
            -> img002.png
            -> img003.png
            -> (...)

        Parameters
        ----------

        Raises
        ------
        ValueError
            If folder is a blank string

        Returns
        -------
        """
        if len(folder) <= 0:
            raise ValueError("folder can't be blank")

        folder = os.listdir(self.__main_folder + '/' + self.__object + '/' + folder + '/')

        print(self.__main_folder + '/' + self.__object + '/' + str(folder) + '/')

        for content in folder:

            print('\t', content)

    def get_folder_contents(self):
        """
        Returns content of folder in self.__dataset_path

        Parameters
        ----------

        Raises
        ------

        Returns
        Array containing string value - name of all files in self.__dataset_path
        """
        return os.listdir(self.__dataset_path)

    def get_dataset(self):
        """
        Returns value of currently chosen dataset

        Parameters
        ----------

        Raises
        ------

        Returns
        Value of __dataset
        """
        return self.__dataset

    def get_main_folder(self):
        """
        Returns value of currently set __main_folder

        Parameters
        ----------

        Raises
        ------

        Returns
        Value of __main_folder
        """
        return self.__main_folder

    def get_current_dataset_path(self):
        """
        Returns value of currently set dataset_path

        Parameters
        ----------

        Raises
        ------

        Returns
        Value of __dataset_path
        """
        return self.__dataset_path

    def get_folder_contents_from_log(self, log_filename='log.txt'):
        """
        Method function is silmillar to get_folder_contents but returns images not from folder contents, but from
        log file that may be stored in folder with images in case some more data was saved regarding UAV flight
        conditions/parameters. In case this data in needed for analysis this method allows for saving only those images
        that have that data saved in log, which would protect dataset from data pollution.

        Parameters
        ----------
        log_filename : str
            Name of file containing logs about conditions/parameters of UAV flight during registration of dataset

        Raises
        ------
        FileNotFoundError:
            If no log file as specified in self.__dataset_path + '/' + log_filename was found

        Returns
        Images names stored as str, Log as panda
        """

        all_files = self.get_folder_contents()

        for file in all_files:

            if file == log_filename:

                log = pd.read_csv(self.__dataset_path + '/' + log_filename,
                                  sep="\t",
                                  header=None,
                                  skiprows=1,
                                  error_bad_lines=False)

                file_names = log[10]

                file_names.pop(0)

                return file_names, log

        raise FileNotFoundError('No log.txt file found')

    def open_img_from_path(self, img_file_name):
        """
        Reads and returns image from self.__dataset_path + img_file_name

        Parameters
        ----------
        img_file_name : str
        Full name of image for example img0001.png

        Raises
        ------
        ValueError
            If img_file_name is blank

        Returns
        Value of __dataset_path
        """
        if len(img_file_name) <= 0:
            raise ValueError("img_file_name can't be blank")

        return io.imread(self.__dataset_path + img_file_name)

    @staticmethod
    def open_img_from_full_path(main_folder, object, dataset, img_file_name):
        """
        Reads and returns image from full absolute path set by 4 parameters in following way:
        main_folder + "/" + object + "/" + dataset + "/" + img_file_name
        Structure must resemble the following:

        data - main folder
        -> boar - object
            -> jurata - dataset
                -> IM_200.jpg - img_file_name

        Parameters
        ----------
        main_folder : str
            Absolute path to main folder
        object : str
            Name of folder containing datasets for one object class
        dataset : str
            Name of folder within object folder containing images
        img_file_name : str
            Full name of image for example img0001.png

        Raises
        ------
        ValueError
            If main_folder is blank
        ValueError
            If object is blank
        ValueError
            If dataset is blank
        ValueError
            If img_file_name is blank

        Returns
        Value of __dataset_path
        """
        if len(main_folder) <= 0 or len(object) <= 0 or len(dataset) <= 0 or len(img_file_name) <= 0:
            raise ValueError("All parameters must be set")

        return io.imread(main_folder + "/" + object + "/" + dataset + "/" + img_file_name)


"""
KOD TESTOWY

test = LocalDataStorage()
test.change_main_folder('D:/magisterka/antrax')
test.choose_data('sarna', '2021-02-04T204006')
print(test.get_folder_contents())
file_names, log = test.get_folder_contents_from_log()
print(log[0][1])
"""
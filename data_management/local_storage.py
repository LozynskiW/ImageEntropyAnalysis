import os
import pandas as pd
from skimage import io


class on_disk:
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

    def get_folder_content(self, folder_name):
        """
        Returns list of all files in self.__main_folder + '/' + self.__object + '/' + folder_name

        Parameters
        ----------
        folder_name : str
            Folder which content is going to be returned

        Raises
        ------

        Returns
        Value of __dataset_path
        """
        return os.listdir(self.__main_folder + '/' + self.__object + '/' + folder_name)

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
from data_management.local_storage import on_disk
from application_management.analysis_progress_memory import file_memory
import pandas as pd
from application_management.util.util import load_data_from_db, db_management
from data_visualisation.plotting_facade import Plots2D, Plots3D, Heatmap
from data_management.data_base.nosql import Mongo
from data_visualisation.consts.plot_options import PlotOptions
from data_unification.data_unification_facade import DataUnificationForPlotting


class AppManager:
    """
    A class used to support the LocalDataStoraga, DataBase and ImageEntropyAnalysis classes to ensure the cooperation
    between the local data processing machine and the database
    """

    def __init__(self, image_processing_system=None):
        # Dependencies
        self.__data_base = Mongo()
        self.__local_storage = on_disk()
        self.__image_processing_system = image_processing_system
        self.__data_unification_for_plotting = DataUnificationForPlotting()

        # Local storage and database coordinates for data extraction
        self.__object = None
        self.__dataset = None

        # Cache memory
        self.__data_from_db = {}

    @property
    def data_base(self):
        return self.__data_base

    @property
    def local_storage(self):
        return self.__local_storage

    @property
    def image_processing_blackbox(self):
        return self.__image_processing_system

    @property
    def object(self):
        return self.__object

    @object.setter
    def object(self, object):
        self.__object = object

    @property
    def dataset(self):
        return self.__dataset

    @dataset.setter
    def dataset(self, dataset):
        self.__dataset = dataset

    def is_already_in_db(self, object, dataset, image):
        try:
            return len(self.__data_base.find_specific(self.__data_base.query_assistance().form_query_to_find_image(
                object=object,
                dataset=dataset,
                image=image))) > 0
        except AttributeError:
            return False

    def __update_or_add_to_db(self, query_to_find_file=None, json_document=None, update=False):

        if json_document is None:
            json_document = {}
        if query_to_find_file is None:
            raise ValueError("No query_to_find_file specified")

        if self.__data_base.is_document_in_db(query=query_to_find_file):

            if update:
                self.__data_base.update_in_db(
                    query=query_to_find_file,
                    json_file=self.__data_base.query_assistance().form_query_to_update(json_document)
                )
            else:
                print('Image:', query_to_find_file, 'is already in database')

        else:
            self.__data_base.put_to_db(json_file=json_document)

    def set_image_processing_system(self, image_processing_system):
        self.__image_processing_system = image_processing_system

    def delete_from_db(self, query, multiple_delete=False):
        self.__data_base.delete_in_db(query, multiple_delete=multiple_delete)

    def set_data(self, object, folder):
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

    def set_object(self, object):
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

    def set_dataset_folder(self, folder):
        self.__local_storage.choose_data(self.__object, folder)
        self.__dataset = folder

    def set_main_folder(self, folder_path):
        self.__local_storage.set_main_folder(folder_path)

    def get_object(self):
        return self.__object

    def get_dataset(self):
        return self.__dataset

    def set_information_processing_blackbox(self, information_processing_blackbox):
        self.__image_processing_system = information_processing_blackbox

    def set_data_from_db(self, data_from_db):

        self.__data_from_db = {}

        if data_from_db:

            self.__data_from_db[self.__object] = data_from_db

        self.__data_from_db['meta'] = {
            "num_of_objects": 1,
            "objects": [self.__object]
        }

    def append_new_object_data_to_data_from_db(self, new_data_from_db):

        self.__data_from_db[self.__object] = new_data_from_db

        self.__data_from_db['meta']['objects'].append(self.__object)
        self.__data_from_db['meta']['num_of_objects'] += 1

    def get_data_from_db(self):
        return self.__data_from_db

    def get_local_storage(self):
        return self.__local_storage

    def get_data_base(self):
        return self.__data_base

    def update_data(self, query, data):
        self.__data_base.update_in_db(query=query, json_file=self.__data_base.query_assistance().form_query_to_update(data))

    def __db_collection_setup(self):
        try:
            self.__data_base.choose_collection(self.__object)
        except AttributeError:
            self.__data_base.create_collection(self.__object)

    def __images_and_logs_setup(self, logs=True):

        if logs:
            try:
                dataset, log = self.__local_storage.get_folder_contents_from_log()

                if len(dataset) > 0:

                    return dataset, log

                else:
                    self.__images_and_logs_setup(logs=False)
            except FileNotFoundError:
                self.__images_and_logs_setup(logs=False)

        else:

            try:
                dataset = self.__local_storage.get_folder_contents()
                return dataset, None
            except FileNotFoundError:
                print("No folder was found, try setting other dataset path")
                return None

    def analyze_dataset(self, logs=False, save_to_db=False, update=False, verbose_mode=False, show_images=False, memory=False):

        if memory:
            memory_unit = file_memory()

        analysis_system = self.__image_processing_system

        self.__db_collection_setup()

        datasets, log = self.__images_and_logs_setup(logs=logs)

        for dataset in datasets:

            self.__local_storage.set_dataset(dataset)
            images = self.__local_storage.get_folder_content(folder_name=dataset)

            for image_name in images:
                query_to_find_file = {'object': self.__object, 'dataset': dataset, 'file_name': image_name}
                json_document_to_db = {'object': self.__object, 'dataset': dataset, 'file_name': image_name}

                if verbose_mode: print({'object': self.__object, 'dataset': dataset, 'file_name': image_name})

                if memory:
                    if memory_unit.is_img_already_processed(self.__object, dataset, image_name):
                        continue

                image = self.__local_storage.open_img_from_path(image_name)

                img_processing_outcome = analysis_system.search_for_target(img=image, verbose_mode=verbose_mode,
                                                                           show_images=show_images)

                for key in img_processing_outcome.keys():
                    json_document_to_db[key] = img_processing_outcome[key]

                if verbose_mode: print(json_document_to_db)

                if save_to_db:
                    self.__update_or_add_to_db(query_to_find_file=query_to_find_file,
                                               json_document=json_document_to_db,
                                               update=update)

                if memory:
                    print(self.__object, dataset, image_name, ' DONE')
                    memory_unit.save_current_img(self.__object, dataset, image_name)

    def plot_2d(self, plot_options: PlotOptions):
        return Plots2D(data_from_db=self.__data_from_db[self.__object], plot_options=plot_options)

    def heatmap(self, plot_options: PlotOptions):
        return Heatmap(data_from_db=self.__data_from_db[self.__object], plot_options=plot_options)

    def plot_3d(self, plot_options: PlotOptions):
        return Plots3D(data_from_db=self.__data_from_db[self.__object], plot_options=plot_options)

    def load_data_from_db(self):

        return load_data_from_db(
            data_base=self.__data_base,
            local_storage=self.__local_storage,
            query_assistance=self.__data_base.query_assistance(),
            object=self.__object)

    def data_base_management(self):
        return db_management(data_base=self.data_base)

    def save_to_excel(self):
        data_sheet = pd.DataFrame(self.__data_from_db)
        data_sheet.to_excel('test.xlsx')
        print("saved to test.xlsx")

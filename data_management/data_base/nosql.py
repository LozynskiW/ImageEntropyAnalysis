import pymongo
import os
import pandas as pd
from skimage import io


class Mongo:
    """
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
        self.__client = pymongo.MongoClient("mongodb://localhost:27017")
        self.__db_database = self.__client["ThermoVisionEntropyAnalysis"]
        self.__db_collection = None

    def check_if_collection_exists(self, collection):

        collection_list = self.__db_database.list_collection_names()

        return collection in collection_list

    def choose_collection(self, collection):

        if not self.check_if_collection_exists(collection):
            raise AttributeError('No such collection in db')

        self.__db_collection = self.__db_database[collection]

    def create_collection(self, collection):

        if self.check_if_collection_exists(collection):
            raise AttributeError('Collection already in db')

        self.__db_database.create_collection(collection)

    def put_to_db(self, json_file):

        if type(json_file) is not dict:
            raise ValueError("json_file mus be dict")

        try:
            self.__db_collection.insert_one(json_file)
        except:
            print("Error in DataBase.put_to_db")

    def delete_in_db(self, query, multiple_delete=False, verbose_mode=True, delete_all=False):

        if query == {} and delete_all == False:
            raise ValueError("query is empty, as a result all documents are going to be updated")

        if multiple_delete:
            self.__db_collection.delete_many(query)
        else:
            self.__db_collection.delete_one(query)

        if verbose_mode:
            print('DELETED: ', query)

    def update_in_db(self, query, json_file, verbose_mode=True, update_all=False):

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

        # datasets = query['dataset']['$in']

        documents_list = self.__db_collection.find(query, {"_id": 0})

        out = []

        for x in documents_list:

            out.append(x)
        # nie wiadomo po co to było
        # query_results_dist = self.__reformat_data_to_dict(datasets=datasets, data_from_db=out)

        return out

    def is_document_in_db(self, query):

        return len(self.find_specific(query=query)) > 0

    def list_collections(self):

        collection_list = self.get_collections()

        for col in collection_list:
            print(col)

    def get_collections(self):

        return self.__db_database.list_collection_names()

    def list_all_documents_passing_query(self, query):

        documents_list = self.__db_collection.find(query, {"_id": 0})

        for x in documents_list:
            print(x)

    @staticmethod
    def __reformat_data_to_dict(datasets, data_from_db):

        data_in_dict = {}

        if not datasets:
            datasets = list(set(map(lambda x: x['dataset'], data_from_db)))

        for d in datasets:
            data_in_dict[d] = list(filter(lambda x: x['dataset'] == d, data_from_db))

        return data_in_dict

    @staticmethod
    def get_query_assistance():

        return Mongo.query_assistance

    class query_assistance:

        @staticmethod
        def form_query_to_update_all(is_valid, was_processed, is_target_detected,
                                     entropy_of_processed_image, entropy_of_original_image,
                                     expected_value_of_processed_image, expected_value_of_original_image,
                                     variance_of_processed_image, variance_of_original_image,
                                     fill_factor, target_coordinates,
                                     horizontal_angle, vertical_angle,
                                     distance_to_object,
                                     histogram):

            return {"$set": {"is_valid": is_valid,
                             "was_processed": was_processed,
                             "is_target_detected": is_target_detected,
                             "entropy_of_processed_image": entropy_of_processed_image,
                             "entropy_of_original_image": entropy_of_original_image,
                             "expected_value_of_processed_image": expected_value_of_processed_image,
                             "expected_value_of_original_image": expected_value_of_original_image,
                             "variance_of_processed_image": variance_of_processed_image,
                             "variance_of_original_image": variance_of_original_image,
                             "fill_factor": fill_factor,
                             "target_coordinates": target_coordinates,
                             "horizontal_angle_of_view": horizontal_angle,
                             "vertical_angle_of_view": vertical_angle,
                             "distance_to_object": distance_to_object,
                             "histogram": histogram}}

        @staticmethod
        def form_query_to_find_image(object, dataset, image):
            return {"object": object, "dataset": dataset, "image": image}

        @staticmethod
        def form_query_to_update(query):

            update_query = {"$set": {}}

            for key in query.keys():
                if key not in ["object", "dataset", "image"]:
                    update_query["$set"][key] = query[key]

            return update_query

        @staticmethod
        def form_query_to_get_multiple_datasets(object, datasets, is_valid=True, was_processed=True,
                                                is_target_detected=True):

            if not object:
                raise AttributeError("No object set")

            query = {
                "object": object,
                "dataset": {"$in": datasets},
                "is_valid": is_valid,
                "was_processed": was_processed,
                "is_target_detected": is_target_detected
            }

            if not datasets:
                del query['dataset']

            if is_valid is None:
                del query['is_valid']

            if was_processed is None:
                del query['was_processed']

            if is_target_detected is None:
                del query['is_target_detected']

            return query
class load_data_to_cache:

    def __init__(self, data_base, local_storage, query_assistance, object):
        self.__local_storage = local_storage
        self.__data_base = data_base
        self.__query_assistance = query_assistance
        self.__object = object

    def test(self, datasets, is_valid=True, was_processed=True,
                          is_target_detected=True):

        query = self.__query_assistance.form_query_to_get_multiple_datasets(
            object=self.__object,
            datasets=datasets,
            is_valid=is_valid,
            was_processed=was_processed,
            is_target_detected=is_target_detected
        )

        try:
            data_from_db = self.__data_base.find_specific(query)
        except RuntimeError:
            return []

        print("Data loaded from DB")
        for k in data_from_db.keys():
            print("key: ", k, " len: ", len(data_from_db[k]))
            print("\tExample data: ", data_from_db[k][0])

    @DeprecationWarning
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

    def multiple_datasets(self, datasets, is_valid=True, was_processed=True,
                          is_target_detected=True):

        query = self.__query_assistance.form_query_to_get_multiple_datasets(
            object=self.__object,
            datasets=datasets,
            is_valid=is_valid,
            was_processed=was_processed,
            is_target_detected=is_target_detected
        )

        try:
            data_from_db = self.__data_base.find_specific(query)
        except RuntimeError:
            return []

        return data_from_db

    def custom_data(self, query):

        try:
            data_from_db = self.__data_base.find_specific(query)
        except RuntimeError:
            return []

        return data_from_db

class db_management:

    def __init__(self, data_base):

        self.__data_base = data_base


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

    def delete_from_db(self, query, multiple_delete=False):
        self.__data_base.delete_in_db(query, multiple_delete=multiple_delete)
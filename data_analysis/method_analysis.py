class overall_data_analysis:

    def __init__(self, data, data_name=""):

        self.__data = data
        self.__data_name = data_name

    def general_description(self):

        print("Dataset: ", self.__data_name)
        if len(self.__data) > 0:

            print("Selected dataset consisted of:", len(self.__data), "images")
            print("")
            print("valid to all: ", str(len(list(map(lambda x: x['is_valid'], self.__data)))), str(len(list(map(lambda x: x['is_valid'], self.__data)))/len(self.__data)))
            print("processed to all: ", str(len(list(map(lambda x: x['was_processed'], self.__data)))), str(len(list(map(lambda x: x['was_processed'], self.__data))) / len(self.__data)))
            print("detected to all: ", str(len(list(map(lambda x: x['is_target_detected'], self.__data)))), str(len(list(map(lambda x: x['is_target_detected'], self.__data))) / len(self.__data)))
            print("")

        else:
            print("Selected dataset consisted of:", len(self.__data), "images")
            print("")
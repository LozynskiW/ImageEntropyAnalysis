@NotImplemented
class AnalyzeHistogram:

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

                    self.__data_base.delete_documents({
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
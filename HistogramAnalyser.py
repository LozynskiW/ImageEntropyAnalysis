import numpy as np
from matplotlib import pyplot as plt
from InformationGainAnalysis.InformationEntropyAnalysis import StatisticsParameters as StatParam
from pyitlib import discrete_random_variable as drv


class HistogramAnalyser:
    def __init__(self):
        self.histogram_from_data = np.zeros(256)
        self.__mean_histogram_from_data = np.zeros(256)
        self.number_of_histograms = 0
        self.__patterns = []
        self.__classes_of_obj = []

    def get_mean_histogram(self):
        return self.__mean_histogram_from_data

    def get_saved_histogram(self):
        return self.histogram_from_data

    def get_saved_histogram_as_query(self):
        out = []

        for num in self.get_mean_histogram():
            out.append(num)

        return {'data': out}

    def add_patterns_from_db(self, data):
        self.__patterns = data
        self.__select_all_classes_of_objects(data)

    def get_patterns(self):
        return self.__patterns

    def __select_all_classes_of_objects(self, pattern_data):

        classes = []

        for p in pattern_data:
            if p['object'] not in classes:
                classes.append(p['object'])

        self.__classes_of_obj = classes

    def compare_with_all_patterns(self, target_histogram):

        if self.does_array_contains_nan(target_histogram):
            return 0

        outcome = {}
        for c in self.__classes_of_obj:
            outcome[c] = 0.0

        for p in self.__patterns:

            self.__mean_histogram_from_data = p['histogram']['data']

            if self.does_array_contains_nan(self.__mean_histogram_from_data):
                print('it works?')
                continue

            mutual_inf = self.calculate_mutual_information(target_histogram)

            for c in self.__classes_of_obj:
                if c == p['object']:
                    if outcome.get(c) < mutual_inf:
                        outcome[c] = mutual_inf

        return outcome

    @staticmethod
    def does_array_contains_nan(array):

        if np.isnan(sum(array)):
            return True
        return False

    def add_histogram_from_im(self, im):
        grayscale, grayscale_prob = StatParam.image_histogram_with_offset(im, "on", 1)
        self.number_of_histograms += 1
        for i in range(0, len(self.histogram_from_data)):
            self.histogram_from_data[i] += grayscale_prob[i]

    def add_histogram_from_db(self, db_res):
        if db_res:
            grayscale_prob = db_res['histogram']['data']
            self.number_of_histograms += 1
            for i in range(0, len(self.histogram_from_data)):
                self.histogram_from_data[i] += grayscale_prob[i]

    def calculate_mean_histogram(self):
        for i in range(0, len(self.histogram_from_data)):
            if self.number_of_histograms != 0:
                self.__mean_histogram_from_data[i] = self.histogram_from_data[i] / self.number_of_histograms
            else:
                self.__mean_histogram_from_data[i] = 0

        self.__mean_histogram_from_data[0] = 0

    def is_saved_histogram_valid(self):
        p = 0
        for i in range(0, len(self.__mean_histogram_from_data)):
            p += self.__mean_histogram_from_data[i]
        if 1.05 > p >= 0.95:
            return True
        else:
            return False

    def do_histograms_match(self, image_with_obj_found):
        histogram_check = []
        grayscale, grayscale_prob = StatParam.image_histogram_with_offset(image_with_obj_found, 'on', 1)
        for i in range(0, len(self.__mean_histogram_from_data)):
            histogram_check.append(grayscale_prob[i] / self.__mean_histogram_from_data[i])
        sum_histogram_check = np.sum(histogram_check) / len(histogram_check)
        self.compare_histograms(grayscale_prob)
        if sum_histogram_check > 0.9:
            return True
        else:
            return False

    @staticmethod
    def calculate_mutual_information_static(X, Y):
        """the reduction in uncertainty of X given Y"""
        return drv.information_mutual(X, Y, 2)

    def calculate_mutual_information(self, Y):
        """the reduction in uncertainty of X given Y"""
        return drv.information_mutual(Y, self.__mean_histogram_from_data, 2)

    def restart(self):
        self.histogram_from_data = np.zeros(256)
        self.__mean_histogram_from_data = np.zeros(256)

    def is_histogram_valid(self):
        return sum(self.get_mean_histogram()) > 0.95

    def show_histogram(self):
        plt.figure(0)
        ox = []
        for i in range(1, len(self.__mean_histogram_from_data)):
            ox.append(i)
        plt.bar(ox, self.__mean_histogram_from_data[1:len(self.__mean_histogram_from_data)])
        plt.xlabel("histogram bins")
        plt.ylabel("histogram data")
        plt.show()

    def compare_histograms(self, histogram_data):
        fig, axs = plt.subplots(2)
        fig.suptitle('Vertically stacked subplots')

        ox = []
        for i in range(1, len(self.__mean_histogram_from_data)):
            ox.append(i)

        axs[0].bar(ox, self.__mean_histogram_from_data[1:len(self.__mean_histogram_from_data)])
        axs[0].set_title('pattern')
        axs[1].bar(ox, histogram_data[1:len(histogram_data)])
        axs[1].set_title('examined')
        plt.show()


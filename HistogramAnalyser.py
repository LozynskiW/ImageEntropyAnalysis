import numpy as np
from matplotlib import pyplot as plt
from InformationGainAnalysis.InformationEntropyAnalysis import StatisticsParameters as StatParam
from pyitlib import discrete_random_variable as drv


class HistogramAnalyser:
    def __init__(self):
        self.histogram_from_data = np.zeros(256)
        self.__mean_histogram_from_data = np.zeros(256)
        self.number_of_histograms = 0

    def get_mean_histogram(self):
        return self.__mean_histogram_from_data

    def get_saved_histogram(self):
        return self.histogram_from_data

    def get_saved_histogram_as_query(self):
        out = []
        for num in self.get_mean_histogram():
            out.append(num)
        return {'data': out}

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
            self.__mean_histogram_from_data[i] = self.histogram_from_data[i] / self.number_of_histograms
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
    def calcualte_mutual_information_static(X, Y):
        """the reduction in uncertainty of X given Y"""
        return drv.information_mutual(X, Y, 2)

    def calcualte_mutual_information(self, Y):
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


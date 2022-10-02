from PIL import Image
from matplotlib import image, cm
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from scipy import ndimage
from scipy.stats import entropy
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import mpl_toolkits.mplot3d.art3d as art3d
from moviepy.editor import VideoFileClip
import statistics as stat
from skimage import data, feature, img_as_uint, img_as_ubyte
from scipy import misc, ndimage
import imageio
from skimage import io
from skimage.color import rgb2grey
import csv
from decimal import Decimal
import json

"""
ALGORYTM:
1. Segmentacja - progowanie / sobel lub prewitt
2. Pomiar entropii
3. Poszukiwanie obrazu na którym entropia jest największa, ale mniejsza niż obrazu przed progowaniem
"""


def low_high_pass_filter(im, filter_type="high", filter_size=9):
    """
    Funkcja do filtrowania obrazu filtrem dolno lub górnoprzepustowym
    Działanie: splot macierzy filtra z obrazem poprzez bibliotekę np i metodę convolve
    :param im:
    :param filter_type:
    :param filter_size:
    :return:
    """
    im = image_type_validation(im)
    if filter_size % 2 == 0:
        filter_size += 1
    filter = [[1 for x in range(filter_size)] for y in range(filter_size)]
    if filter_type == "high":
        for x in range(0, filter_size):
            for y in range(filter_size):
                if x == np.floor(filter_size / 2) and y == np.floor(filter_size / 2):
                    filter[x][y] = 1 - 1 / filter_size
                else:
                    filter[x][y] = - 1 / filter_size
    elif filter_type == "low":
        for x in range(filter_size):
            for y in range(filter_size):
                filter[x][y] = np.round(1 / filter_size, 2)

    im_filtered = ndimage.convolve(im, filter)
    return im_filtered


def histogram_mean_shift(im, mean_shift_value):
    szer = len(im[0])
    wys = len(im)
    im = rgb2grey(im)
    for x in range(0, szer):
        for y in range(0, wys):
            im[y][x] -= mean_shift_value
            if im[y][x] < 0:
                im[y][x] = 0
    return im


def information_threshold(im):
    """
    Metoda pozwalająca na segmentowanie obrazu poprzez progowanie. Próg obliczany jest na podstawie informacyjności
    poszczególnych odcieni szarości z przestrzeni barw (skali szarości). Warunkiem pozostawienia piksela jest wartość
    informacyjności powyżej średniej
    :param im:
    :return:
    """
    szer = len(im[0])
    wys = len(im)
    im = rgb2grey(im)
    grayscale, gray_shade_prob, H, H_n, I_n = information_entropy(im)
    mean_information = stat.mean(I_n)
    for x in range(0, szer):
        for y in range(0, wys):
            if I_n[im[y][x]] < mean_information:
                im[y][x] = 0
    return im


def global_threshold(im):
    """
    Funkcja służąca do segmentacji obrazu przy wykorzystaniu progu globalnego
    :param im:
    :return:
    """
    """
        Instrukcje walidujące format obrazu wejściwoego (obraz jest w formacie uint8 i w skali szarości)
        """
    im = image_type_validation(im)
    gray_shades, gray_shades_prob = image_histogram(im, "on")

    deltaT = 1
    T = 1

    while True:
        T_old = T
        """
        Zmienne do wyznaczenia threshold metodą otsu
        """
        # początkowy próg
        m1 = 0  # srednia wartość intensywnosci pikseli w przedziale do k
        m2 = 0  # srednia wartość intensywnosci pikseli w przedziale od k do 255
        p1 = 0  # prawdopodobieństwo wystąpienia piksela z przedziału do k
        p2 = 0  # prawdopodobieństwo wystąpienia piksela z przedziału od k do 255

        p1 = sum(gray_shades_prob[0:T])
        p2 = sum(gray_shades_prob[T:len(gray_shades_prob)])

        for i in gray_shades:
            pi = gray_shades_prob[i]
            if i < T:
                m1 = m1 + i * pi
            else:
                m2 = m2 + i * pi

        if p1 != 0:
            m1 = m1 / p1
        else:
            m1 = m1 / T

        if p2 != 0:
            m2 = m2 / p2
        else:
            m2 = m2 / (255 - T)

        T = (m1 + m2) / 2

        if T_old - T < deltaT:
            break

    return T


def otsu_threshold(im):
    """
    Funkcja służąca do segmentacji obrazu przy wykorzystaniu progu obliczonego metodą OTSU
    :param im:
    :return:
    """

    im = image_type_validation(im)

    gray_shades, gray_shades_prob = image_histogram(im, "on")

    optimal_k = 0
    best_ni = 0
    mg = 0  # srednia wartość wszystkich pikseli
    delta_g2 = 0  # wariancja wartosci ze skali szarosci

    for i in gray_shades:
        mg = mg + i * gray_shades_prob[i]

    for i in gray_shades:
        delta_g2 = gray_shades_prob[i] * (i - mg) ** 2 + delta_g2

    for k in range(1, len(gray_shades)):
        """
        Zmienne do wyznaczenia threshold metodą otsu
        """
        # początkowy próg
        m1 = 0  # srednia wartość intensywnosci pikseli w przedziale do k
        m2 = 0  # srednia wartość intensywnosci pikseli w przedziale od k do 255
        p1 = 0  # prawdopodobieństwo wystąpienia piksela z przedziału do k
        p2 = 0  # prawdopodobieństwo wystąpienia piksela z przedziału od k do 255
        ni = 0  # parametr określający poprawność wyboru przedziału

        delta_b2 = 0  # wariancja pomiędzy przedziałami

        p1 = sum(gray_shades_prob[0:k])
        p2 = sum(gray_shades_prob[k:len(gray_shades_prob)])

        for i in gray_shades:
            pi = gray_shades_prob[i]
            if i < k:
                m1 = m1 + i * pi
            else:
                m2 = m2 + i * pi

        if p1 != 0:
            m1 = m1 / p1
        else:
            m1 = m1 / k

        if p2 != 0:
            m2 = m2 / p2
        else:
            m2 = m2 / (255 - k)

        delta_b2 = ((mg - m1) ** 2) * (p1 * p2)
        ni = delta_b2 / delta_g2

        if ni > best_ni:
            best_ni = ni
            optimal_k = k

    return optimal_k


def threshold_segmentation(im, T):
    """
    Metoda do usuwania z obrazu pikseli poniżej progu, metoda przypisuje im wartość równą 0
    :param im:
    :param T:
    :return:
    """
    show_image(im)
    im = image_type_validation(im)
    im_out = im.copy()
    szer = len(im[0])
    wys = len(im)
    # print("Próg = ", T)
    for x in range(0, szer):
        for y in range(0, wys):
            if im[y][x] < T:
                im_out[y][x] = 0
    show_image(im_out)
    plt.show()
    return im_out


def search_for_object(information_segmented_im, edge_segmented_image):
    """
    Metoda do wyszukiwania obiektu na obrazie.
    Działanie: metoda sprawdza położenie pikseli o intensywności wyższej od 0 na obrazie uzyskanym z detekcji konturowej,
    następnie przeszukuje otoczenie tego piksela w obrazie segemntowanym na podstawie informacyjności.
    Wybrany zostaje obszar o największej gęstości pikseli, następnie obszar ten jest powiększany, dopóki w jego oteczeniu
    są piksele o wartości >0
    :param information_segmented_im:
    :param edge_segmented_image:
    :return:
    """
    szer = len(information_segmented_im[0])
    wys = len(information_segmented_im)

    window_width = int(szer / 40)
    window_height = int(wys / 40)

    im_out = information_segmented_im.copy()
    highest_mean = 0
    obj_x = 0
    obj_y = 0

    action = 0
    """Pierwszy etap - wyszukanie miejsca o największej średniej wartości pikseli"""
    for y in range(0, wys):
        for x in range(0, szer):
            if edge_segmented_image[y][x] > 0 and information_segmented_im[y][x] > 0:
                mean = 0
                num = 0
                for yw in range(0, window_height):
                    for xw in range(0, window_width):
                        try:
                            mean += information_segmented_im[y + yw][x + xw]
                            num += 1
                        except:
                            mean += 0
                mean = mean / num
                if mean > highest_mean:
                    highest_mean = mean
                    obj_x = x
                    obj_y = y
    """
        stan na 17.01 22:34 wszystko działa
        for y in range(0, wys):
            for x in range(0, szer):
                if edge_segmented_image[y][x] > 0:
                    mean = 0
                    num = 0
                    for yw in range(0, window_height):
                        for xw in range(0, window_width):
                            try:
                                if information_segmented_im[y + yw][x + xw] > 0:
                                    mean += information_segmented_im[y + yw][x + xw]
                                    num += 1
                            except:
                                mean += 0
                    if num > 0:
                        mean = mean / num
                    if mean > highest_mean:
                        highest_mean = mean
                        obj_x = x
                        obj_y = y

    """

    """Drugi etap - automatyczne rozszerzenie okna"""
    still_search = True
    while still_search:
        still_search = False
        sum = [0, 0]
        num = [0, 0]
        means = [0, 0]
        # print(window_height, window_width)
        for yw in range(0, window_height):
            for xw in range(0, window_width):
                try:
                    if ((xw == 0) and (0 <= yw < window_height)) or ((yw == 0) and (0 <= xw < window_width)):
                        sum[0] += information_segmented_im[obj_y + yw][obj_x + xw]
                        num[0] += 1

                    if ((xw == window_width - 1) and (0 <= yw < window_height)) or (
                            (yw == window_height - 1) and (0 <= xw < window_width)):
                        sum[1] += information_segmented_im[obj_y + yw][obj_x + xw]
                        num[1] += 1
                except:
                    still_search = False

        for i in range(0, len(sum)):
            if sum[i] != 0 and num[i] != 0:
                means[i] = sum[i] / num[i]
            else:
                means[i] = 0

        if means[0] > 0:
            obj_x -= 1
            window_width += 1
            obj_y -= 1
            window_height += 1
            still_search = True
        if means[1] > 0:
            window_width += 1
            window_height += 1
            still_search = True

    # usuwanie pikseli poza okieniem
    for y in range(0, wys):
        for x in range(0, szer):
            if not ((obj_y - window_height <= y < obj_y + window_height) and (
                    obj_x - window_width <= x < obj_x + window_width)):
                im_out[y][x] = 0

            """ kod do obrysowywania okienka, należy usunąć przed testowaniem
            
            if (x == obj_x) and (obj_y <= y < obj_y+window_height):
                im_out[y][x] = 255
            if (x == obj_x + window_width - 1) and (obj_y <= y < obj_y+window_height):
                im_out[y][x] = 255
            if (y == obj_y) and (obj_x <= x < obj_x + window_width):
                im_out[y][x] = 255
            if (y == obj_y+window_height - 1) and (obj_x <= x < obj_x+window_width):
                im_out[y][x] = 255
            """
    return im_out


def show_image(im):
    plt.figure()
    plt.imshow(im, cmap=gray())
    plt.show()


def rgb_to_rgba(im):
    szer = len(im[0])
    wys = len(im)
    im_rgba = im.copy()
    im_rgba = np.float32(im_rgba)
    for x in range(0, szer):
        for y in range(0, wys):
            im_rgba[y][x][0] = im_rgba[y][x][0] / 255
            im_rgba[y][x][1] = im_rgba[y][x][1] / 255
            im_rgba[y][x][2] = im_rgba[y][x][2] / 255
            np.append(im_rgba[y][x], [1])
    return im_rgba


def entropy_video_analysis(video_path):
    clip = VideoFileClip(video_path)
    entropy_vector = []
    frame = 0
    for frames in clip.iter_frames():
        x, y, H, Hn, In = information_entropy(frames)
        print(frame, H)
        entropy_vector.append(H)
        frame += 1
    print('Najwięcej informacji zawarto w klatce', entropy_vector.index(min(entropy_vector)))


def entropy3d_view(H_n, im, im_overlay='off'):
    """
    Metoda do wizualizacji informacyjności pikseli na wykresie 3D
    :param H_n:
    :param im:
    :param im_overlay:
    :return:
    """
    szer = len(im[0])
    wys = len(im)
    if im_overlay == 'on':
        im_rgba = rgb_to_rgba(im)
    im = image_type_validation(im)

    im_grid = np.outer(np.zeros((wys,)), np.linspace(0, szer - 1, szer))
    im_rgba_grid = im_grid.copy()
    ox = np.outer(np.ones((wys,)), np.linspace(0, szer - 1, szer))
    oy = np.outer(np.ones((szer,)), np.linspace(wys - 1, 0, wys))
    oy = oy.T
    for x in range(0, szer):
        for y in range(0, wys):
            im_grid[y][x] = H_n[int(im[y][x])]

    """Wyświetlenie obrazu pod wykresem"""
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.view_init(elev=90., azim=270)
    ax.plot_surface(ox, oy, im_grid, cmap=get_cmap('jet'), alpha=0.5)
    if im_overlay == 'on':
        ax.plot_surface(ox, oy, im_rgba_grid, rstride=5, cstride=5, facecolors=im_rgba)
    plt.show()
    return im_grid


def information_entropy(im):
    """
    Metoda obliczająca entropię informacji na obrazie
    :param im:
    :return:
    """
    im = image_type_validation(im)

    # Histogram - dyskretny rozkład prawdopodobieństwa
    grayscale, gray_shade_prob = image_histogram(im, "on")

    I_n = []  # informacja zawarta w pikselu

    # Entropia
    H_n = []  # entropia od n
    for p in gray_shade_prob:
        if p == 0:
            I = 0
        else:
            I = -np.log2(p)
        H = p * I
        H_n.append(H)
        I_n.append(I)
    H = np.sum(H_n)  # wartosc entropii
    return grayscale, gray_shade_prob, H, H_n, I_n


def image_luminosity_test(im_mean_histogram_value, test_mean_histogram_value, test_std_dev):
    if im_mean_histogram_value < test_mean_histogram_value + test_std_dev:
        return True
    return False


def image_histogram(im, normalize="off"):
    """
    Funkcja służąca do obliczania histogramu z obrazu
    :param im:
    :return:
    """
    # im = image_type_validation(im)
    szer = len(im[0])
    wys = len(im)
    grayscale = []  # wektor skali szarości
    for i in range(0, 256):
        grayscale.append(i)
    gray_shade_prob = np.zeros(len(grayscale))  # wektor prawdopodobieństw odcieni szarości

    for y in range(0, wys):
        for x in range(0, szer):
            try:
                gray_shade_prob[im[y][x]] += 1
            except TypeError:
                print("ERROR")
                print(y, x)
                print(im)
                print(im[y][x])
    num = np.sum(gray_shade_prob)  # Ilosc wszystkich pikseli

    # normalizacja
    if normalize == "on":
        for i in range(0, len(gray_shade_prob)):
            gray_shade_prob[i] = gray_shade_prob[i] / num

    return grayscale, gray_shade_prob


def image_histogram_with_offset(im, normalize="off", grayscale_offset=0):
    """
    Funkcja służąca do obliczania histogramu z obrazu
    :param im:
    :return:
    """
    # im = image_type_validation(im)
    szer = len(im[0])
    wys = len(im)
    grayscale = []  # wektor skali szarości
    for i in range(grayscale_offset, 256):
        grayscale.append(i)
    gray_shade_prob = np.zeros(len(grayscale))  # wektor prawdopodobieństw odcieni szarości

    for y in range(0, wys):
        for x in range(0, szer):
            if im[y][x] > grayscale_offset:
                gray_shade_prob[im[y][x]] += 1
    num = np.sum(gray_shade_prob)  # Ilosc wszystkich pikseli

    # normalizacja
    if normalize == "on":
        for i in range(0, len(gray_shade_prob)):
            gray_shade_prob[i] = gray_shade_prob[i] / num

    return grayscale, gray_shade_prob


def mean_from_probability(values_vector, prob_vector):
    mean = 0
    for i in range(0, len(values_vector)):
        mean = mean + values_vector[i] * prob_vector[i]
    return mean


def standard_deviation(mean, value_vector):
    N = 0
    sum = 0
    for i in value_vector:
        sum = sum + (i - mean) ** 2
    sum = sum / N
    return sqrt(sum)


def information_data_comparision(im1, im2):
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2)
    ox, _, H1, H_n1, I_n1 = information_entropy(im1)
    _, _, H2, H_n2, I_n2 = information_entropy(im2)

    fig.suptitle("Porównanie rozkładu entropii i informacyjności na wartość luminancji")
    ax1.bar(ox, H_n1)
    ax2.bar(ox, H_n2)
    ax1.set(xlabel='luminancja pikseli', ylabel='entropia informacji', title="Entropia = " + str(H1))
    ax2.set(xlabel='luminancja pikseli', title="Entropia = " + str(H2))

    ax3.bar(ox, I_n1)
    ax4.bar(ox, I_n2)
    ax3.set(xlabel='luminancja pikseli', ylabel='informacyjność pikseli')
    ax4.set(xlabel='luminancja pikseli')

    ax5.imshow(im1, cmap=gray())
    ax6.imshow(im2, cmap=gray())
    plt.show()


def image_type_validation(im):
    img_gray = rgb2grey(im)
    return img_as_ubyte(img_gray)


class HistogramAnalyser:
    def __init__(self):
        self.histogram_from_data = np.zeros(256)
        self.mean_histogram_from_data = np.zeros(256)
        self.mean_value_of_histogram = 0
        self.most_exp_val_of_histogram = 0
        self.results_path = "/results"

    def set_result_path(self, result_path):
        self.results_path = result_path

    def create_new_data(self, object_name, pre, path, num_of_imgs):
        self.analyse_database(pre, path, num_of_imgs)
        self.show_histogram()
        with open(str(self.results_path) + str(object_name) + '.txt', 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(self.mean_histogram_from_data)

    def load_data(self, object_name):
        with open(str(self.results_path) + str(object_name) + '.txt', 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            new_data = []
            for row in csv_reader:
                if len(row) == len(self.mean_histogram_from_data):
                    for i in range(0, len(self.mean_histogram_from_data)):
                        new_data.append(float(row[i]))
                    self.mean_histogram_from_data = new_data

    def analyse_database(self, pre, path, num_of_imgs):
        for i in range(1, num_of_imgs + 1):
            zeros = ''
            if (pre == "DJI_") and (i < 10):
                zeros = "000"
            elif (pre == "DJI_") and (10 <= i < 100):
                zeros = '00'
            elif (pre == "DJI_") and (100 <= i < 1000):
                zeros = '0'
            img_path = path + pre + str(zeros) + str(i) + "_res.jpg"
            try:
                print("Analyzing image #", i)
                img = io.imread(img_path)
            except:
                print("No sych file as: ", img_path, " searching on")
            else:
                img_gray = rgb2grey(img)
                img_gray = img_as_ubyte(img_gray)
                edges2 = feature.canny(img_gray, sigma=2)
                im_information_seg = information_threshold(img_gray)
                im_segmented = search_for_object(im_information_seg, edges2)
                self.add_histogram(im_segmented)
        self.calculate_mean_histogram()

    def add_histogram(self, im):
        grayscale, grayscale_prob = image_histogram_with_offset(im, "on", 1)
        for i in range(0, len(self.histogram_from_data)):
            self.histogram_from_data[i] += grayscale_prob[i]

    def calculate_mean_histogram(self):
        for i in range(0, len(self.histogram_from_data)):
            self.mean_histogram_from_data[i] = self.histogram_from_data[i]

    def check_saved_histogram(self):
        p = 0
        for i in range(0, len(self.mean_histogram_from_data)):
            p += self.mean_histogram_from_data[i]
        if p >= 0.95:
            return True
        else:
            return False

    def check_histograms_match(self, im):
        img_gray = rgb2grey(im)
        img_gray = img_as_ubyte(img_gray)
        edges2 = feature.canny(img_gray, sigma=2)
        im_information_seg = information_threshold(img_gray)
        im_segmented = search_for_object(im_information_seg, edges2)
        grayscale, grayscale_prob = image_histogram(im_segmented, "on")
        histogram_check = []
        for i in range(0, len(self.mean_histogram_from_data)):
            histogram_check.append(grayscale_prob[i] / self.mean_histogram_from_data[i])
        sum_histogram_check = np.sum(histogram_check) / len(histogram_check)

        self.compare_histograms(grayscale_prob)
        if sum_histogram_check > 0.8:
            return True
        else:
            return False

    def show_histogram(self):
        plt.figure(0)
        ox = []
        for i in range(1, len(self.mean_histogram_from_data)):
            ox.append(i)
        plt.bar(ox, self.mean_histogram_from_data[1:len(self.mean_histogram_from_data)])
        plt.xlabel("histogram bins")
        plt.ylabel("histogram data")
        plt.show()

    def compare_histograms(self, histogram_data):
        fig, axs = plt.subplots(2)
        fig.suptitle('Vertically stacked subplots')

        ox = []
        for i in range(1, len(self.mean_histogram_from_data)):
            ox.append(i)

        axs[0].bar(ox, self.mean_histogram_from_data[1:len(self.mean_histogram_from_data)])
        axs[0].set_title('pattern')
        axs[1].bar(ox, histogram_data[1:len(histogram_data)])
        axs[1].set_title('examined')
        plt.show()

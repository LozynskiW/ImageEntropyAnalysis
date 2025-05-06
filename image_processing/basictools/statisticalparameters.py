"""
    Container for static methods used to calculate statistical parameters of images like histogram and it's parameters,
    entropy, information, information gain
"""
import array

import numpy as np
from numpy import copy

from image_processing.models.image import ArrayImage


def image_histogram(im, normalize_to_pdf=False, grayscale_offset=-1):
    """
    Parameters
    ----------
    im : np.array
        Image used to calculate histogram
    normalize_to_pdf: bool
        Parameter enabling normalization of histogram to probability distribution function (each value of histogram
        divided by sum of all pixels)
    grayscale_offset: int
        Offset of luminance value (grayscale value of image) allowing to calculate histogram without some grayscale
        values, for example if grayscale_offset == 2 then histogram is calculated for values [2:255]

    Raises
    ------

    Returns
    -------
    """

    szer = len(im[0])
    wys = len(im)
    grayscale = []  # wektor skali szarości

    for i in range(0, 256):
        grayscale.append(i)
    gray_shade_prob = np.zeros(len(grayscale))  # wektor prawdopodobieństw odcieni szarości

    for y in range(0, wys):
        for x in range(0, szer):

            if im[y][x] > grayscale_offset:
                gray_shade_prob[im[y][x]] += 1

    num = np.sum(gray_shade_prob)  # Ilosc wszystkich pikseli

    # normalizacja
    if normalize_to_pdf:
        for i in range(0, len(gray_shade_prob)):
            gray_shade_prob[i] = gray_shade_prob[i] / num

    return grayscale, gray_shade_prob


def normalize_histogram(histogram_values_counts: array) -> array:
    num_of_all_pixels = np.sum(histogram_values_counts)
    probabilities = copy(histogram_values_counts)

    for i in range(0, len(probabilities)):
        probabilities[i] = probabilities[i] / num_of_all_pixels

    return probabilities


def information_gain_between_histograms(original_img_histogram, processed_img_histogram):
    """
    Calculates information gain between original_img_histogram and processed_img_histogram

    Parameters
    ----------
    original_img_histogram : np.array
        Array or list containing probabilities for each luminance value where index of element is it's luminance value
        For example if 1st element is 0.002 then probability of getting pixel luminance of value 1 is 0.002
    processed_img_histogram: np.array
        Same as original_img_histogram but contains probabilities for processed histogram

    Raises
    ------

    Returns
    -------
    information_gain : float
        Information gain between histograms
    """
    information_gain = 0

    for i in range(0, len(processed_img_histogram)):

        if processed_img_histogram[i] * original_img_histogram[i] > 0:
            information_gain += original_img_histogram[i] * np.log2(
                original_img_histogram[i] / processed_img_histogram[i])

    return information_gain


def exp_val_from_histogram(grayscale, gray_shade_prob):
    """
    Calculates expected value from histogram where probabilities for values are not all equal. Expected value
    is calculated in following way:
    E = Sum( P(X) * X )

    Parameters
    ----------
    grayscale : np.array
        Array or list containing values of grayscale color space used to calculate expected value
    gray_shade_prob: np.array
        Array or list containing probabilities for values of grayscale color space

    Raises
    ------

    Returns
    -------
    exp_val : float
        Expected value for given histogram
    """

    exp_val = 0

    for i in range(0, len(grayscale)):
        exp_val += grayscale[i] * gray_shade_prob[i]

    return exp_val


def variance_from_histogram(grayscale, gray_shade_prob, mean_value):
    variance = 0
    for i in range(0, len(grayscale)):
        variance += ((grayscale[i] - mean_value) ** 2) * gray_shade_prob[i]
    return variance


def std_dev_from_histogram(variance):
    return np.sqrt(variance)


def std_dev_from_variance(variance: float):
    return np.sqrt(variance)


def information_entropy(im):
    """
    Information entropy calculated by:
    H = sum (p * log2(p)) [bit]
    where:
    p - probability of pixel value (color/luminescence) in image histogram
    :param im: grayscale image
    :returns: information entropy for given image and array of information entropy for each value of pixel
    """
    # Histogram - dyskretny rozkład prawdopodobieństwa
    grayscale, gray_shade_prob = image_histogram(im, True)

    I_n = information(im)

    # Entropia
    H_n = []  # entropia od n

    for i in range(0, len(I_n)):
        H = gray_shade_prob[i] * I_n[i]

        H_n.append(H)

    H = np.sum(H_n)  # wartosc entropii

    return H, H_n


def information(im):
    """
    Information calculated by:
    I = log2(p) [bit]
    where:
    p - probability of pixel value (color/luminescence) in image histogram
    :param im: grayscale image
    :returns: array of information for each value of pixel
    """
    # Histogram - dyskretny rozkład prawdopodobieństwa
    grayscale, gray_shade_prob = image_histogram(im, True)

    I_n = []  # informacja zawarta w pikselu

    for p in gray_shade_prob:

        if p == 0:
            I = 0
        else:
            I = -np.log2(p)

        I_n.append(I)

    return I_n


def information_for_image_histogram(image: ArrayImage):
    """
    Information calculated by:
    I = log2(p) [bit]
    where:
    p - probability of pixel value (color/luminescence) in image histogram
    :returns: array of information for each value of pixel
    """

    histogram_values, histogram_probabilities = image_histogram(image, True)

    information_for_histogram_values = []

    for p in histogram_probabilities:
        information_for_histogram_values.append(-np.log2(p) if p != 0 else 0)

    return histogram_values, information_for_histogram_values


def information_entropy_for_image_histogram(image: ArrayImage):
    """
    Information entropy calculated by:
    H(x) = p(x) * log2(p(x)) [bit]
    where:
    p - probability of pixel value (color/luminescence) in image histogram
    :param image: grayscale image
    :returns: information entropy for given image and array of information entropy for each value of pixel
    """

    histogram_values, histogram_probabilities = image_histogram(image, True)

    _, information_for_histogram_values = information_for_image_histogram(image)

    information_entropy_for_histogram_values = []

    for i in range(0, len(histogram_values)):
        H_i = histogram_probabilities[i] * information_for_histogram_values[i]
        information_entropy_for_histogram_values.append(H_i)

    return histogram_values, information_entropy_for_histogram_values


def calculate_all(im):
    grayscale, gray_shade_prob = image_histogram(im, True)
    mean = exp_val_from_histogram(grayscale, gray_shade_prob)
    var = variance_from_histogram(grayscale, gray_shade_prob, mean)
    std_dev = std_dev_from_histogram(var)
    entropy, _ = information_entropy(im)
    return mean, var, std_dev, entropy

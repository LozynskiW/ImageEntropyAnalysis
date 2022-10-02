import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm


def show_images_before_and_after(img_before_processing, img_after_processing, fig_title):
    """
    Shows subplot with 2 images side by side

    Parameters
    ----------
    img_before_processing : image
       Image ploted on the left side of subplot

    img_before_processing : image
       Image ploted on the right side of subplot

    fig_title : string
       Title of figure

    Raises
    ------

    Returns
    -------
    """
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    fig.suptitle(fig_title)
    ax1.imshow(img_before_processing, cmap='Greys')
    ax2.imshow(img_after_processing, cmap='Greys')
    plt.show()


def calculate_fill_factor(img, normalise=True):
    """
    Calculates number of pixels that have luminance greater than 0 - pixels represented by value more than 0

    Parameters
    ----------
    img : image
       Image to calculate fill factor from

    normalise : bool
       If True enables normalising fill factor to number of pixels - fill_factor/(img_width*img_height)

    Raises
    ------

    Returns
    fill_factor - number of pixels that have value greater than 0
    """
    img_width = len(img[0])
    img_height = len(img)

    fill_factor = 0

    for x in range(0, img_width):

        for y in range(0, img_height):

            if img[y][x] > 0:
                fill_factor += 1

    if normalise:
        fill_factor /= (img_width * img_height)
        return np.around(fill_factor, decimals=2)
    else:
        return fill_factor


def enumerate_list(list_to_enumerate):
    """
    Prints all elements of given array

    Parameters
    ----------
    list_to_enumerate : list
        list that elements are going to be enumerated

    Raises
    ------
    AttributeError
        If list_to_enumerate is not list

    Returns
    -------
    """

    if type(list_to_enumerate) is not list:
        raise AttributeError("Parameter must be python list")

    for i in range(0, len(list_to_enumerate)):
        print(i, list_to_enumerate[i])


class StatisticsParameters:
    """
    Container for static methods used to calculate statistical parameters of images like histogram and it's parameters,
    entropy, information, information gain

    Attributes
    ----------
    """

    @staticmethod
    def image_histogram(im, normalize_to_pdf=False, grayscale_offset=-1):
        """
        Checks if collection is in currently set __db_database. If it is then method returns True, if not False

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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def variance_from_histogram(grayscale, gray_shade_prob, mean_value):
        """
        Calculates variance value from image histogram

        Parameters
        ----------
        grayscale : np.array
            Array or list containing values of grayscale color space used to calculate expected value
        gray_shade_prob: np.array
            Array or list containing probabilities for values of grayscale color space
        mean_value: float/int
            Mean value for given histogram. If not specified it's value is calculated via exp_val_from_histogram method
            from same class

        Raises
        ------

        Returns
        -------
        variance : float
            Variance for given histogram
        """

        if not mean_value:
            mean_value = StatisticsParameters.exp_val_from_histogram(grayscale, gray_shade_prob)

        variance = 0
        for i in range(0, len(grayscale)):
            variance += ((grayscale[i] - mean_value) ** 2) * gray_shade_prob[i]
        return variance

    @staticmethod
    def std_dev_from_variance(variance):
        """
        Calculates standard deviation from given variance

        Parameters
        ----------
        variance : float
            Variance of histogram

        Raises
        ------

        Returns
        -------
        std_dev : float
            sqrt(variance)
        """
        return np.sqrt(variance)

    @staticmethod
    def information_entropy(img):
        """
        Calculates information entropy of given image in bits as classic Shannon definition of entropy:
        E(X) = Sum ( P(x) * -log2(P(x)) ) for x in gray_scale_prob

        Parameters
        ----------
        img : image
            Uint8, grayscale image

        Raises
        ------

        Returns
        -------
        H : float
            Information entropy calculated from entire image
        H_n : list
            Information entropy for each luminance value
        """
        # Histogram
        grayscale, gray_shade_prob = StatisticsParameters.image_histogram(img, True)

        I_n = StatisticsParameters.information(img)

        # Entropy for each probability (n)
        H_n = []

        for i in range(0, len(I_n)):
            H = gray_shade_prob[i] * I_n[i]

            H_n.append(H)

        # Entropy for image
        H = np.sum(H_n)

        return H, H_n

    @staticmethod
    def information(img):
        """
        Calculates information in bits that each luminance value of pixel has according to Shannon theory:
        I(x) =  -log2(P(x)) ) for x in gray_scale_prob

        Parameters
        ----------
        img : image
            Uint8, grayscale image

        Raises
        ------

        Returns
        -------
        I_n : list
            Information entropy for each luminance value
        """
        # Histogram - dyskretny rozkład prawdopodobieństwa
        grayscale, gray_shade_prob = StatisticsParameters.image_histogram(img, True)

        I_n = []  # informacja zawarta w pikselu

        for p in gray_shade_prob:

            if p == 0:
                I = 0
            else:
                I = -np.log2(p)

            I_n.append(I)

        return I_n

    @staticmethod
    def calculate_all(img):
        """
        Calculates grayscale luminance vector, histogram, expected value, variance and standard deviation of histogram,
        entropy of histogram for image
        I(x) =  -log2(P(x)) ) for x in gray_scale_prob

        Parameters
        ----------
        img : image
            Uint8, grayscale image

        Raises
        ------

        Returns
        -------
        grayscale : list
            Information entropy for each luminance value
        gray_shade_prob : list
            Information entropy for each luminance value
        mean : float
            Information entropy for each luminance value
        var : float
            Information entropy for each luminance value
        std_dev : float
            Information entropy for each luminance value
        entropy : float
            Information entropy for each luminance value
        """
        grayscale, gray_shade_prob = StatisticsParameters.image_histogram(img, True)
        mean = StatisticsParameters.exp_val_from_histogram(grayscale, gray_shade_prob)
        var = StatisticsParameters.variance_from_histogram(grayscale, gray_shade_prob, mean)
        std_dev = StatisticsParameters.std_dev_from_variance(var)
        entropy, _ = StatisticsParameters.information_entropy(img)
        return mean, var, std_dev, entropy


class TwoDimStructures:

    @staticmethod
    def center_disk_mask(img, size_factor=2):
        """
        Calculates mask that would only leave pixels in image center (based on circle) useful when it is assumed that
        outside of image center is noise

        Parameters
        ----------
        img : image
            Uint8, grayscale image

        Raises
        ------

        Returns
        -------
        outer_disk_mask : bool image
            Mask leaving only pixels in image center
        """
        nrows, ncols = img.shape

        row, col = np.ogrid[:nrows, :ncols]

        cnt_row, cnt_col = nrows / 2, ncols / 2

        outer_disk_mask = ((row - cnt_row) ** 2 + (col - cnt_col) ** 2 > (nrows / size_factor) ** 2)

        return outer_disk_mask

    @staticmethod
    def gkern(cols, rows, nsig=1):
        """Returns a 2D Gaussian kernel."""

        x = np.linspace(-nsig, nsig, cols + 1)
        kern1d_x = np.diff(norm.cdf(x))

        y = np.linspace(-nsig, nsig, rows + 1)
        kern1d_y = np.diff(norm.cdf(y))

        kern2d = np.outer(kern1d_y, kern1d_x)
        return kern2d / kern2d.sum()


class ImageOverlay:

    @staticmethod
    def __check_is_img_and_mask_shape_equal(img, mask):

        if img.shape == mask.shape:
            return True

        raise ValueError("Shape of mask and img is not equal")

    @staticmethod
    def image_and(img, mask):

        ImageOverlay.__check_is_img_and_mask_shape_equal(img, mask)

        width = len(img[0])
        height = len(img)
        im_out = img.copy()

        for y in range(0, height):

            for x in range(0, width):

                if img[y][x] > 0 and mask[y][x]:
                    im_out[y][x] = img[y][x]

        return im_out

    @staticmethod
    def image_multiply(img, mask):

        ImageOverlay.__check_is_img_and_mask_shape_equal(img, mask)

        width = len(img[0])
        height = len(img)
        im_out = img.copy()

        for y in range(0, height):

            for x in range(0, width):
                im_out[y][x] = img[y][x] * mask[y][x]

        return im_out

    @staticmethod
    def image_add(img, mask):

        ImageOverlay.__check_is_img_and_mask_shape_equal(img, mask)

        width = len(img[0])
        height = len(img)
        im_out = img.copy()

        for y in range(0, height):

            for x in range(0, width):

                if img[y][x] > 0 and mask[y][x]:
                    im_out[y][x] = img[y][x] + mask[y][x]

        return im_out

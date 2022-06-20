import numpy as np
from matplotlib import pyplot as plt


def show_image_before_and_after(img_before_processing, img_after_processing, fig_title):

    fig, (ax1, ax2) = plt.subplots(ncols=2)
    fig.suptitle(fig_title)
    ax1.imshow(img_before_processing, cmap='Greys')
    ax2.imshow(img_after_processing, cmap='Greys')
    plt.show()


def show_images_before_and_after(imgs_before_processing, img_after_processing, fig_title):

    fig, axs = plt.subplots(2, len(imgs_before_processing))
    fig.suptitle(fig_title)

    for i in range(0, len(imgs_before_processing)):
        axs[0, i].imshow(imgs_before_processing[i], cmap='Greys')

    axs[1, 0].imshow(img_after_processing, cmap='Greys')
    plt.show()


def calculate_fill_factor(img):
    img_width = len(img[0])
    img_height = len(img)

    fill_factor = 0

    for x in range(0, img_width):

        for y in range(0, img_height):

            if img[y][x] > 0:
                fill_factor += 1

    fill_factor /= (img_width * img_height)

    return np.around(fill_factor*100, decimals=2)


def enumerate_list(list_to_enumerate):
    """
    Used for communication with data base and CRUD operations execution

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
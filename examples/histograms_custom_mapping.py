import math

import matplotlib
import numpy as np

from data_visualisation.models import PlotOptions, FigureOptions, PlotColor
from application_management.app import AppManager
from data_visualisation._implementations.heatmap import HeatmapConfig
from data_visualisation.models import FigureOptions
from consts.system_util import PATH_TO_MAIN_FOLDER, PATH_TO_FIGURES_FOLDER
from data_visualisation.plotting_facade import PlottingFacade
from matplotlib import pyplot as plt


def create_bins(min_value, max_value, step) -> np.ndarray:
    return np.arange(start=min_value, stop=max_value + 1, step=step, dtype=int)


def calculate_counts_for_bins(histogram: list | np.ndarray, bins: list | np.ndarray, offset=0):
    counts_for_bins = np.zeros(len(bins))

    current_bin_index = 0

    for val_index in range(offset, len(histogram)):

        if val_index < bins[current_bin_index]:
            counts_for_bins[current_bin_index] += histogram[val_index]
        else:
            current_bin_index += 1

    return counts_for_bins


def distances_list(distance_x_z_list: list[tuple]) -> list[str]:
    return list(
        map(lambda x_z_tuple: str(int(math.sqrt(math.pow(x_z_tuple[0], 2) + math.pow(x_z_tuple[1], 2))))+" [m]", distance_x_z_list))


def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current Axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(range(data.shape[1]), labels=col_labels,
                  rotation=-30, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max()) / 2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


app_manager = AppManager()
app_manager.set_main_folder(PATH_TO_MAIN_FOLDER)

path_to_save_figures = f'{PATH_TO_FIGURES_FOLDER}'

objects = [
    'sphere', 'cube', 'cone', 'cylinder'
]

datasets_for_objects = [
    'white_only', 'gradient', 'white_noise'
]

x_z_coordinates_pairs = [(10, 10), (20, 20), (40, 40), (80, 80), (140, 140), (200, 200)]

grayscale_histogram_values = np.linspace(1, 255, num=254)

bins_num = 16
max_histogram_value = 256
step = int(max_histogram_value / bins_num)
bins_for_histogram = create_bins(min_value=step, max_value=max_histogram_value, step=step)

for obj in objects:
    app_manager.set_object(object=obj)
    # multiple_plot = PlottingFacade.multiple_plot().scatter_plot(figure_options)

    for dataset in datasets_for_objects:
        data_for_obj = (app_manager
                        .load_data_from_db()
                        .custom_data({"dataset": dataset}))

        histogram_data = np.zeros((len(x_z_coordinates_pairs), len(bins_for_histogram)))

        for data_for_image in data_for_obj:

            x = data_for_image["x"]
            z = data_for_image["z"]

            if not (x, z) in x_z_coordinates_pairs:
                continue

            histogram = data_for_image["histogram_of_processed_image"]

            bins_counts = calculate_counts_for_bins(histogram, bins_for_histogram, offset=1)

            y = x_z_coordinates_pairs.index((x, z))

            for x_val_index in range(0, len(bins_counts)):
                histogram_data[y][x_val_index] = bins_counts[x_val_index]

        fig, ax = plt.subplots()

        im = heatmap(histogram_data, distances_list(x_z_coordinates_pairs), bins_for_histogram, ax=ax, vmin=0,
                        cmap="magma_r", cbarlabel=f"{obj}_{dataset}")

        texts = annotate_heatmap(im, valfmt="{x:.1f}")

        fig.tight_layout()
        fig.set_size_inches(12, 5)
        plt.title(f"histogram bins structure for: {obj}, dataset: {dataset}")
        # plt.show()
        plt.savefig(f"{path_to_save_figures}/histogram_bins_structure_{obj}_{dataset}.png", dpi=600)

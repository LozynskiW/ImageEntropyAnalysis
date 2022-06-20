import numpy as np
from scipy.stats import norm


def center_disk_mask(img):
    nrows, ncols = img.shape

    row, col = np.ogrid[:nrows, :ncols]

    cnt_row, cnt_col = nrows / 2, ncols / 2

    outer_disk_mask = ((row - cnt_row) ** 2 + (col - cnt_col) ** 2 > (nrows / 2) ** 2)

    return outer_disk_mask


def gaussian_kernel(cols, rows, nsig=1):
    """Returns a 2D Gaussian kernel."""

    x = np.linspace(-nsig, nsig, cols + 1)
    kern1d_x = np.diff(norm.cdf(x))

    y = np.linspace(-nsig, nsig, rows + 1)
    kern1d_y = np.diff(norm.cdf(y))

    kern2d = np.outer(kern1d_y, kern1d_x)
    return kern2d / kern2d.sum()
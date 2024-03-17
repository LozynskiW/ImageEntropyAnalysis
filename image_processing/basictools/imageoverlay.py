"""
    Methods used to fuse two images into one
"""
def __check_is_img_and_mask_shape_equal(img, mask):

    if img.shape == mask.shape:
        return True

    raise ValueError("Shape of mask and img is not equal")


def image_and(img, mask):

    __check_is_img_and_mask_shape_equal(img, mask)

    width = len(img[0])
    height = len(img)
    im_out = img.copy()

    for y in range(0, height):

        for x in range(0, width):

            if img[y][x] > 0 and mask[y][x]:
                im_out[y][x] = img[y][x]

    return im_out


def image_multiply(img, mask):

    __check_is_img_and_mask_shape_equal(img, mask)

    width = len(img[0])
    height = len(img)
    im_out = img.copy()

    for y in range(0, height):

        for x in range(0, width):
            im_out[y][x] = img[y][x] * mask[y][x]

    return im_out


def image_add(img, mask):

    __check_is_img_and_mask_shape_equal(img, mask)

    width = len(img[0])
    height = len(img)
    im_out = img.copy()

    for y in range(0, height):

        for x in range(0, width):

            if img[y][x] > 0 and mask[y][x]:
                im_out[y][x] = img[y][x] + mask[y][x]

    return im_out
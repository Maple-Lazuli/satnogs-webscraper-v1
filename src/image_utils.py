import os

from PIL import Image
from collections import Counter
import numpy as np


def find_left_bound(im):
    left_lengths = []
    x_max, y_max = im.size
    for y in range(0, y_max):
        for x in range(0, x_max):
            if im.getpixel((x, y)) != (255, 255, 255, 255):
                left_lengths.append(x)
                break
    return Counter(left_lengths).most_common(1)[0][0]


def find_upper_bound(im):
    upper_lengths = []
    x_max, y_max = im.size
    for x in range(0, x_max):
        for y in range(0, y_max):
            if im.getpixel((x, y)) != (255, 255, 255, 255):
                upper_lengths.append(y)
                break
    return Counter(upper_lengths).most_common(1)[0][0]


def find_bottom_bound(im):
    bottom_lengths = []
    x_max, y_max = im.size
    for x in range(0, x_max):
        for y in range(y_max - 1, 0, -1):
            if im.getpixel((x, y)) != (255, 255, 255, 255):
                bottom_lengths.append(y)
                break
    return Counter(bottom_lengths).most_common(1)[0][0]


def find_right_bound(im):
    x_max, y_max = im.size
    for x in range(x_max // 2, x_max):
        broke = False
        for y in range(0, y_max):
            if im.getpixel((x, y)) != (255, 255, 255, 255):
                broke = True
                break
        if not broke:
            return x


def crop_and_save_psd(input_image, delete_original=True):
    im_source = Image.open(input_image)

    # Find the boundaries of the center most PSD and crop the image.
    left_bound = find_left_bound(im_source)
    right_bound = find_right_bound(im_source)
    upper_bound = find_upper_bound(im_source)
    bottom_bound = find_bottom_bound(im_source)
    im_cropped = im_source.crop([left_bound, upper_bound, right_bound, bottom_bound])

    # Convert to greyscale and save as unit8 bytes to disk, using the original file name, minus the file extension
    numpy_im = np.array(im_cropped.convert('L'))

    # store the shape and write to a file
    shape = numpy_im.shape
    new_file_name = input_image[:-4]
    numpy_im.tofile(new_file_name)

    # remove the original, larger image
    if delete_original:
        os.remove(input_image)

    return shape, new_file_name

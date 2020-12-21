import random
from math import sqrt
from random import choices


def calc_grid_size(number_of_shapes):
    y = round(sqrt(number_of_shapes))
    if y * y >= number_of_shapes:
        return [y, y]
    else:
        return [y + 1, y]


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def indexes_to_rgb(colors, indexes_list):
    rgb_list = []
    colors_len = len(colors)
    colors_list = list(colors.values())
    for index in indexes_list:
        nr = round(index) % colors_len
        color = colors_list[nr]
        rgb_list.append(rgb2hex(color[0], color[1], color[2]))
    return rgb_list

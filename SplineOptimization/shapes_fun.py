import random
from math import sqrt
from random import choices


def calc_grid_size(number_of_shapes):
    y = round(sqrt(number_of_shapes))
    if y * y >= number_of_shapes:
        return [y, y]
    else:
        return [y + 1, y]


def calc_shape_colors(number_of_shapes, colors, colors_probability):
    return choices([rgb2hex(a[0], a[1], a[2]) for c, a in colors.items()],
                   weights=colors_probability, k=number_of_shapes)


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


def list_of_shapes_colors(ratios, colors, seriesFromRatios,stats):
    colors_indexes = []
    keys = list(colors.keys())
    keys.pop()  # pop last color (background color)
    if ratios:
        for index, phase in enumerate(keys):
            if len(seriesFromRatios[phase]) > 0:
                for i in range(len(seriesFromRatios[phase][ratios[0].lower()])):
                    colors_indexes.append(index)
    else:
        colors_weights = [weight for weight in stats['onePointprobability'].values()]
        colors_weights.pop()
        colors_indexes = random.choices(range(0, len(keys)), weights=colors_weights, k=12)

    return colors_indexes

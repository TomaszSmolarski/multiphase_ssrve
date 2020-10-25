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


def list_of_shapes_colors(ratios, colors, seriesFromRatios, stats, background_color_key):
    colors_indexes = []
    indexes_dict = {phase: index for index, phase in enumerate(colors.keys())}
    indexes_dict.pop(background_color_key)
    if ratios:
        for phase, index in indexes_dict.items():
            if len(seriesFromRatios[phase]) > 0:
                for i in range(len(seriesFromRatios[phase][ratios[0].lower()])):
                    colors_indexes.append(index)
        if len(colors_indexes) > 25:
            colors_weights = [weight for phase, weight in stats['onePointprobability'].items() if
                              phase != background_color_key]
            colors_indexes = random.choices(list(indexes_dict.values()), weights=colors_weights, k=25)
    else:
        colors_weights = [weight for phase, weight in stats['onePointprobability'].items() if
                          phase != background_color_key]
        colors_indexes = random.choices(list(indexes_dict.values()), weights=colors_weights, k=25)

    return colors_indexes

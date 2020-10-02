import io
import math
from functools import reduce
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np
from random import choices
from math import sqrt
import cv2


def create_ssrve_image(knots, shapes_colors, background_color,
                       x_size=800, y_size=600, dpi=100):
    curves = [not_intersecting_polygen(curve) for curve in knots]
    plt = pyplot_config(background_color, x_size, y_size, dpi)
    return make_open_cv_image(curves, shapes_colors, x_size, y_size, plt)


def calc_grid_size(number_of_shapes):
    y = round(sqrt(number_of_shapes))
    if y * y >= number_of_shapes:
        return [y, y]
    else:
        return [y + 1, y]


def calc_shape_colors(number_of_shapes, colors, colors_probability):
    return choices([rgb2hex(a[0], a[1], a[2]) for c, a in colors.items()],
                   weights=colors_probability, k=number_of_shapes)


def indexes_to_rgb(colors, indexes_list):
    rgb_list = []
    colors_len = len(colors)
    colors_list = list(colors.values())
    for index in indexes_list:
        nr = round(index) % colors_len
        color = colors_list[nr]
        rgb_list.append(rgb2hex(color[0], color[1], color[2]))
    return rgb_list


def pyplot_config(background_color, x_size, y_size, dpi):
    plt.figure(figsize=(x_size / dpi, y_size / dpi), dpi=dpi,
               facecolor=rgb2hex(background_color[0], background_color[1], background_color[2]),
               )
    # no coordinate system
    ax = plt.axes([0, 0, 1, 1], frameon=False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # to make normal shape of picture, not cut empty space
    plt.plot([0, x_size, x_size, 0, 0], [0, 0, y_size, y_size, 0],
             alpha=0)
    # no scaled shapes
    plt.autoscale(tight=True)
    return plt


def make_open_cv_image(curves, shapes_colors, x_size, y_size, plt):
    for nr, ctrp in enumerate(curves):
        ctr = np.array(ctrp)
        x = ctr[:, 0]
        y = ctr[:, 1]

        l = len(x)

        t = np.linspace(0, 1, l - 2, endpoint=True)
        t = np.append([0, 0, 0], t)
        t = np.append(t, [1, 1, 1])

        # u, tck = interpolate.splprep([x, y], k=3, s=0)
        # u = np.linspace(0, 1, num=50, endpoint=True)
        # out = interpolate.splev(u, tck)

        tck = [t, [x, y], 3]
        u3 = np.linspace(0, 1, (max(l * 2, 70)), endpoint=True)
        out = interpolate.splev(u3, tck)

        x = [x_el if x_size >= x_el >= 0
             else 0 if x_el < 0
        else x_size for x_el in out[0]]

        y = [y_el if y_size >= y_el >= 0
             else 0 if y_el < 0
        else y_size for y_el in out[1]]

        plt.fill(x, y, color=shapes_colors[nr],
                 edgecolor=shapes_colors[nr], antialiased=False)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')

    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


def save_to_file(filename, image_open_cv):
    try:
        cv2.imwrite(filename, img=image_open_cv)
    except:
        print('first render file')


def not_intersecting_polygen(array_of_points):
    center = reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), array_of_points, (0, 0))
    center = (center[0] / len(array_of_points), (center[1] / len(array_of_points)))
    array_of_points.sort(key=lambda a: math.atan2(a[1] - center[1], a[0] - center[0]))
    array_of_points.append(array_of_points[0])
    return array_of_points


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def list_of_shapes_colors(ratios, colors, seriesFromRatios):
    colors_list = []
    colors_indexes = []
    keys = list(colors.keys())
    keys.pop()  # pop last color (background color)
    for index, phase in enumerate(keys):
        if len(seriesFromRatios[phase]) > 0:
            color_rgb = colors[phase]
            for i in range(len(seriesFromRatios[phase][ratios[0].lower()])):
                colors_list.append(rgb2hex(color_rgb[0], color_rgb[1], color_rgb[2]))
                colors_indexes.append(index)
    return colors_list, colors_indexes

import io
import math
from functools import reduce
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import cv2
from SplineOptimization.shapes_fun import rgb2hex
from SplineOptimization.periodic_fun import not_period_splines

def create_ssrve_image(knots, shapes_colors, background_color, periodic_type_f,
                       x_size, y_size, dpi=100):
    curves = [not_intersecting_polygen(curve) for curve in knots]
    plt = pyplot_config(background_color, x_size, y_size, dpi)
    return make_open_cv_image(curves, shapes_colors, x_size, y_size, plt, periodic_type_f)


def pyplot_config(background_color, x_size, y_size, dpi):
    mpl.rcParams['savefig.pad_inches'] = 0
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


def not_intersecting_polygen(array_of_points):
    center = reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), array_of_points, (0, 0))
    center = (center[0] / len(array_of_points), (center[1] / len(array_of_points)))
    array_of_points.sort(key=lambda a: math.atan2(a[1] - center[1], a[0] - center[0]))
    array_of_points.append(array_of_points[0])
    return array_of_points


def make_open_cv_image(curves, shapes_colors, x_size, y_size, plt, periodic_type_f):
    for nr, ctrp in enumerate(curves):

        ctr = np.array(ctrp)
        x = ctr[:, 0]
        y = ctr[:, 1]
        l = len(x)
        '''
        tck, u = interpolate.splprep([x, y], k=3, s=0)
        u = np.linspace(0, 1, (max(l * 2, 700)), endpoint=True)
        out = interpolate.splev(u, tck)
        '''
        # interpolate
        t = np.linspace(0, 1, l - 2, endpoint=True)
        t = np.append([0, 0, 0], t)
        t = np.append(t, [1, 1, 1])
        tck = [t, [x, y], 3]
        u3 = np.linspace(0, 1, (max(l * 2, 420)), endpoint=True)
        out = interpolate.splev(u3, tck)

        x, y = periodic_type_f(x_size, y_size, out[0], out[1])

        for x_el, y_el in zip(x, y):
            plt.fill(x_el, y_el, color=shapes_colors[nr],
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

cur = [[[50, 50], [100, 50], [100, 100], [50, 100]]
       ]
sh = ['#111222', '#334455']
bc = (255, 255, 255)
args = (cur,sh,bc,not_period_splines,400,400)
kwargs = {"knots": cur, "shapes_colors":sh, "background_color":bc, "x_size":200, "y_size":300, "periodic_type_f":not_period_splines }
#im = create_ssrve_image(cur, sh, bc, x_size=400, y_size=400, periodic_type_f=period_splines)
def x (kwargs):
    im = create_ssrve_image(**kwargs)
    save_to_file('../aaaa1.png', im)
#im = create_ssrve_image(**kwargs)
#save_to_file('../aaaa2.png', im)
x(kwargs)
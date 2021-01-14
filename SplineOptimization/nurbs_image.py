import io
import math
from functools import reduce
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import cv2
from SplineOptimization.nurbs_periodic import NurbsPeriodic


class NurbsImage(NurbsPeriodic):
    def __init__(self, background_color, x_size, y_size, periodic, plot_dpi=100):
        super().__init__(x_size=x_size, y_size=y_size, periodic=periodic)
        self.background_color = background_color
        self.splines_dpi = 100 if self.periodic_type_f.__name__ == "not_period_nurbs" else 420
        self.plot_dpi = plot_dpi

    def create_ssrve_image(self, knots, shapes_colors):
        curves = [self.__not_intersecting_polygen(curve) for curve in knots]
        plt = self.__pyplot_config()
        return self.__make_open_cv_image(curves, shapes_colors, plt)

    def __pyplot_config(self):
        mpl.rcParams['savefig.pad_inches'] = 0
        plt.figure(figsize=(self.x_size / self.plot_dpi, self.y_size / self.plot_dpi), dpi=self.plot_dpi,
                   facecolor=self.background_color,
                   )
        # no coordinate system
        ax = plt.axes([0, 0, 1, 1], frameon=False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        # to make normal shape of picture, not cut empty space
        plt.plot([0, self.x_size, self.x_size, 0, 0], [0, 0, self.y_size, self.y_size, 0],
                 alpha=0)
        # no scaled shapes
        plt.autoscale(tight=True)
        return plt

    def __not_intersecting_polygen(self, array_of_points):
        points = list(array_of_points)
        center = reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), points, (0, 0))
        center = (center[0] / len(points), (center[1] / len(points)))
        points.sort(key=lambda a: math.atan2(a[1] - center[1], a[0] - center[0]))
        points.append(points[0])
        return points

    def __make_open_cv_image(self, curves, shapes_colors, plt):
        for nr, ctrp in enumerate(curves):
            ctr = np.array(ctrp)
            x = ctr[:, 0]
            y = ctr[:, 1]
            l = len(x)
            t = np.linspace(0, 1, l - 2, endpoint=True)
            t = np.append([0, 0, 0], t)
            t = np.append(t, [1, 1, 1])
            tck = [t, [x, y], 3]
            u3 = np.linspace(0, 1, (max(l * 2, self.splines_dpi)), endpoint=True)
            out = interpolate.splev(u3, tck)
            x, y = self.periodic_type_f(out[0], out[1])
            for x_el, y_el in zip(x, y):
                plt.fill(x_el, y_el, color=shapes_colors[nr],
                         edgecolor=shapes_colors[nr], antialiased=False)
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')

        img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

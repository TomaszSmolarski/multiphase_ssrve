import copy
import functools
import numpy as np

from GrainsOptimization.grain_periodic import GrainPeriodic


class GrainGrowth(GrainPeriodic):
    def __init__(self, height, width, colors_bgr_list, periodic):
        super().__init__(height, width, periodic)
        self.colors_bgr_list = colors_bgr_list

    def __change_gen(self, ssrve, edge_points):
        copy_ssrve = copy.deepcopy(ssrve)
        points_to_check = set()
        for x, y in edge_points:
            if x <= 0 or x >= self.width - 1 or y <= 0 or y >= self.height - 1:
                points_to_check.update(self.periodic_type_f(x, y))
            else:
                points_to_check.update(self.not_period_grid(x, y))

        new_edge_points = set()
        for x, y in points_to_check:
            if functools.reduce(lambda i, j: i and j, map(lambda m, k: m == k,
                                                          ssrve[x][y], (255, 255, 255)), True):
                if x <= 0 or x >= self.width - 1 or y <= 0 or y >= self.height - 1:
                    neighbours_list = self.periodic_type_f(x, y)
                else:
                    neighbours_list = self.not_period_grid(x, y)
                colors_list = self.neighbours_colors_list(ssrve, neighbours_list)
                colors_list = list(filter(
                    lambda a: functools.reduce(lambda i, j: i and j,
                                               map(lambda m, k: m == k, a, (255, 255, 255)),
                                               True) == False, colors_list))
                if len(colors_list) > 0:
                    new_edge_points.add((x, y))
                    copy_ssrve[x][y] = max(set(colors_list), key=colors_list.count)
        return copy_ssrve, new_edge_points

    def create_ssrve_image(self, starting_points):
        ssrve = [[(255, 255, 255) for a in range(self.width)] for b in range(self.height)]
        pts = []
        for x, y, color in starting_points:
            ssrve[x][y] = self.colors_bgr_list[color]
            pts.append((x, y))
        i = 0
        while any((255, 255, 255) in row for row in ssrve):
            ssrve, pts = self.__change_gen(ssrve, pts)
            i += 1
        return np.array(ssrve)

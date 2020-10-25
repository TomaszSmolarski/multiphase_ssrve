import copy
import functools
import numpy as np

from GrainsOptimization.periodic_fun import period_grid, neighbours_colors_list


def change_gen(ssrve, height, width, edge_points, periodic_type_f):
    copy_ssrve = copy.deepcopy(ssrve)
    points_to_check = set()
    for x, y in edge_points:
        if x <= 0 or x >= width - 1 or y <= 0 or y >= height - 1:
            points_to_check.update(periodic_type_f(x, y, height, width))
        else:
            points_to_check.update(period_grid(x, y, height, width))

    new_edge_points = set()
    for x, y in points_to_check:
        if functools.reduce(lambda i, j: i and j, map(lambda m, k: m == k, ssrve[x][y], (255, 255, 255)), True):
            if x <= 0 or x >= width - 1 or y <= 0 or y >= height - 1:
                neighbours_list = periodic_type_f(x, y, height, width)
            else:
                neighbours_list = period_grid(x, y, height, width)

            colors_list = neighbours_colors_list(ssrve, neighbours_list)
            colors_list = list(filter(lambda a:
                                      functools.reduce(lambda i, j: i and j,
                                                       map(lambda m, k: m == k, a, (255, 255, 255)), True)
                                      == False, colors_list))
            if len(colors_list) > 0:
                new_edge_points.add((x, y))
                copy_ssrve[x][y] = max(set(colors_list), key=colors_list.count)

    return copy_ssrve, new_edge_points


def create_ssrve_image(starting_points, height, width, colors_bgr_list, periodic_type_f):
    ssrve = [[(255, 255, 255) for a in range(width)] for b in range(height)]
    pts = []
    for x, y, color in starting_points:
        ssrve[x][y] = colors_bgr_list[color]
        pts.append((x, y))
    while any((255, 255, 255) in row for row in ssrve):
        ssrve, pts = change_gen(ssrve, height, width, pts, periodic_type_f)
    return np.array(ssrve)

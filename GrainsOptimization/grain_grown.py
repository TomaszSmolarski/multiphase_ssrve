import copy
import functools
import numpy as np

from GrainsOptimization.periodic_fun import period_color, period_points


def moore_neighbourhood(row, col, ssrve, height, width):
    neighbourhood_list = []
    neighbourhood_list.append(period_color(ssrve, row - 1, col - 1, height, width))
    neighbourhood_list.append(period_color(ssrve, row - 1, col, height, width))
    neighbourhood_list.append(period_color(ssrve, row - 1, col + 1, height, width))

    neighbourhood_list.append(period_color(ssrve, row + 1, col - 1, height, width))
    neighbourhood_list.append(period_color(ssrve, row + 1, col, height, width))
    neighbourhood_list.append(period_color(ssrve, row + 1, col + 1, height, width))

    neighbourhood_list.append(period_color(ssrve, row, col - 1, height, width))
    neighbourhood_list.append(period_color(ssrve, row, col + 1, height, width))
    return neighbourhood_list


def moore_neighbourhood_inside(row, col, ssrve):
    neighbourhood_list = []
    neighbourhood_list.append(ssrve[row - 1][col - 1])
    neighbourhood_list.append(ssrve[row - 1][col])
    neighbourhood_list.append(ssrve[row - 1][col + 1])

    neighbourhood_list.append(ssrve[row + 1][col - 1])
    neighbourhood_list.append(ssrve[row + 1][col])
    neighbourhood_list.append(ssrve[row + 1][col + 1])

    neighbourhood_list.append(ssrve[row][col - 1])
    neighbourhood_list.append(ssrve[row][col + 1])
    return neighbourhood_list


def moore_neighbourhood_points_inside(row, col):
    neighbourhood_list = []
    neighbourhood_list.append((row - 1, col - 1))
    neighbourhood_list.append((row - 1, col))
    neighbourhood_list.append((row - 1, col + 1))

    neighbourhood_list.append((row + 1, col - 1))
    neighbourhood_list.append((row + 1, col))
    neighbourhood_list.append((row + 1, col + 1))

    neighbourhood_list.append((row, col - 1))
    neighbourhood_list.append((row, col + 1))
    return neighbourhood_list


def moore_neighbourhood_points(row, col, height, width):
    neighbourhood_list = []
    neighbourhood_list.append(period_points(row - 1, col - 1, height, width))
    neighbourhood_list.append(period_points(row - 1, col, height, width))
    neighbourhood_list.append(period_points(row - 1, col + 1, height, width))

    neighbourhood_list.append(period_points(row + 1, col - 1, height, width))
    neighbourhood_list.append(period_points(row + 1, col, height, width))
    neighbourhood_list.append(period_points(row + 1, col + 1, height, width))

    neighbourhood_list.append(period_points(row, col - 1, height, width))
    neighbourhood_list.append(period_points(row, col + 1, height, width))
    return neighbourhood_list


def change_gen(ssrve, height, width, edge_points):
    copy_ssrve = copy.deepcopy(ssrve)
    points_to_check = set()
    for x, y in edge_points:
        if x <= 0 or x >= width - 1 or y <= 0 or y >= height - 1:
            points_to_check.update(moore_neighbourhood_points(x, y, height, width))
        else:
            points_to_check.update(moore_neighbourhood_points_inside(x, y))
    new_edge_points = set()
    for x, y in points_to_check:
        if functools.reduce(lambda i, j: i and j, map(lambda m, k: m == k, ssrve[x][y], (255, 255, 255)), True):

            if x <= 0 or x >= width - 1 or y <= 0 or y >= height - 1:
                neighbours_list = moore_neighbourhood(x, y, ssrve, height, width)

            else:
                neighbours_list = moore_neighbourhood_inside(x, y, ssrve)

            # neighbours_list = moore_neighbourhood(x, y, ssrve, height, width)
            neighbours_list = list(filter(lambda a:
                                          functools.reduce(lambda i, j: i and j,
                                                           map(lambda m, k: m == k, a, (255, 255, 255)), True)
                                          == False, neighbours_list))

            if len(neighbours_list) > 0:
                new_edge_points.add((x, y))
                copy_ssrve[x][y] = max(set(neighbours_list), key=neighbours_list.count)

    return copy_ssrve, new_edge_points


def create_ssrve_image(starting_points, height, width, colors_bgr_list):
    print(starting_points)
    ssrve = [[(255, 255, 255) for a in range(width)] for b in range(height)]

    for x, y, color in starting_points:
        period_x, period_y = period_points(x, y, height, width)
        ssrve[period_x][period_y] = colors_bgr_list[color]

    pts = [(x, y) for x, y, c in starting_points]

    while any((255, 255, 255) in row for row in ssrve):
        ssrve, pts = change_gen(ssrve, height, width, pts)
    return np.array(ssrve)

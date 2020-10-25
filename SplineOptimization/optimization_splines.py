# -*- coding: utf-8 -*-

import math
from random import randrange
from SplineOptimization.shapes_fun import calc_grid_size, indexes_to_rgb, list_of_shapes_colors
from SplineOptimization.ssrve_fun import create_ssrve_image
from default_config import d_threads, d_colors, d_x_size, d_y_size, d_knots_number, \
    d_pop_size, d_ratios, d_ratios_periodic, d_save_dir_path, d_target_series_from_ratios, d_target_stats
from optimization_abstract import AbstractOptimize


class SplineOptimize(AbstractOptimize):
    def __init__(self, picture_path, periodic_type_f, ratios_periodic=d_ratios_periodic, threads=d_threads,
                 colors=d_colors, x_size=d_x_size,
                 y_size=d_y_size,
                 knots_number=d_knots_number, pop_size=d_pop_size, ratios=d_ratios, save_dir_path=d_save_dir_path,
                 target_series_from_ratios=d_target_series_from_ratios, target_stats=d_target_stats):
        super().__init__(picture_path=picture_path, threads=threads, colors=colors,
                         x_size=x_size, y_size=y_size, pop_size=pop_size, ratios=ratios,
                         ratios_periodic=ratios_periodic, save_dir_path=save_dir_path,
                         target_series_from_ratios=target_series_from_ratios, target_stats=target_stats)

        self.knots_number = knots_number
        self.shapes_indexes = list_of_shapes_colors(self.ratios, self.colors, self.target_series_from_ratios,
                                                    self.target_stats, self.background_color_key)
        self.number_of_shapes = len(self.shapes_indexes)
        self.grid_size = calc_grid_size(self.number_of_shapes)
        self.extra_bounding_dist = self.calc_shapes_range_dist()
        self.activation_number = 30
        self.periodic_type_f = periodic_type_f
        self.splines_dpi = 100 if self.periodic_type_f.__name__ == "not_period_splines" else 420

    def calc_shapes_range_dist(self):
        extra_range = [0, 0]  # [math.floor(dist[0]/4),math.floor(dist[1]/4)] # not necessary
        dist = [math.floor(self.x_size / (2 * self.grid_size[0])) + extra_range[0],
                math.floor(self.y_size / (2 * self.grid_size[1])) + extra_range[1]]
        return dist

    '''
    def generate_shapes_range(self):
        extra_range = [0, 0]  # [math.floor(dist[0]/4),math.floor(dist[1]/4)] # not necessary

        dist = [math.floor(self.x_size / (2*self.grid_size[0]))+extra_range[0],
                math.floor(self.y_size / (2*self.grid_size[1]))+extra_range[1]]
        shapes_range = []

        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                if self.grid_size[1] * row + col >= self.number_of_shapes:
                    break
                #full random center point of shape
                x_center = randrange(0, self.x_size)
                y_center = randrange(0, self.y_size)
                # random center point of shape within box
                #x_center = randrange(row * dist[0]*2, (row + 1) * dist[0]*2)
                #y_center = randrange(col * dist[1]*2, (col + 1) * dist[1]*2)
                r = {"x": [x_center - dist[0], x_center + dist[0]],
                     "y": [y_center - dist[1], y_center + dist[1]]}
                shapes_range.append(r)

        return shapes_range, dist
    '''

    def generate_pt(self, random, args):
        shapes_range = []
        for shape_nr in range(self.number_of_shapes):
            # full random center point of shape
            x_center = randrange(0, self.x_size)
            y_center = randrange(0, self.y_size)
            x_dist = randrange(round(self.extra_bounding_dist[0] / 2), 2 * self.extra_bounding_dist[0])
            y_dist = randrange(round(self.extra_bounding_dist[1] / 2), 2 * self.extra_bounding_dist[1])
            r = {"x": [x_center - x_dist,
                       x_center + x_dist],
                 "y": [y_center - y_dist,
                       y_center + y_dist]}
            shapes_range.append(r)
        shapes = []
        for shape in shapes_range:
            for knot_number in range(self.knots_number):
                shapes.append(randrange(shape["x"][0], shape["x"][1]))
                shapes.append(randrange(shape["y"][0], shape["y"][1]))
                shapes.append(randrange(0, 100))  # activation value of point
        shapes.extend(random.sample(self.shapes_indexes, len(self.shapes_indexes)))

        return shapes

    def bound_pt(self, candidate, args):

        for i in range(self.number_of_shapes * self.knots_number):
            candidate[i * 3] = max(min(candidate[i * 3], self.x_size + 2 * self.extra_bounding_dist[0]),
                                   - 2 * self.extra_bounding_dist[0])
            candidate[i * 3 + 1] = max(min(candidate[i * 3 + 1], self.y_size + 2 * self.extra_bounding_dist[1]),
                                       - 2 * self.extra_bounding_dist[1])
            candidate[i * 3 + 2] = max(min(candidate[i * 3 + 2], 100), 0)

        return candidate

    def create_starting_points_from_candidate(self, candidate):
        """
        Zwraca listę list punktów węzłowych [x,y]
        :param candidate:
        :return:
        """
        shapes_colors_list = candidate[-self.number_of_shapes:]
        curves = candidate[:-self.number_of_shapes]
        curves = [curves[i:i + 3] for i in range(0, len(curves), 3)]
        curves = [curves[i:i + self.knots_number] for i in range(0, len(curves), self.knots_number)]
        curves = [[[round(point[0]), round(point[1])] for point in curve if point[2] > self.activation_number] for curve
                  in curves]
        curves = [curve for curve in curves if len(curve) > 2]

        shapes_colors = indexes_to_rgb(self.colors, shapes_colors_list)
        return curves, shapes_colors

    def create_ssrve_image(self, args):
        return create_ssrve_image(*args, background_color=self.background_color, x_size=self.x_size, y_size=self.y_size,
                                  periodic_type_f=self.periodic_type_f, splines_dpi=self.splines_dpi)

    def calc_candidate_fitness(self, starting_points):
        return super().calc_candidate_fitness(starting_points)

    def evaluate_pt(self, candidates, args):
        return super().evaluate_pt(candidates, args)

    def ssrve_observer(self, population, num_generations, num_evaluations, args):
        return super().ssrve_observer(population, num_generations, num_evaluations, args)

    def optimize(self):
        super().optimize()

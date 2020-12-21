# -*- coding: utf-8 -*-

import math
from random import randrange, uniform

from SplineOptimization.shapes_fun import calc_grid_size, indexes_to_rgb
from SplineOptimization.ssrve_fun import create_ssrve_image
from optimization_abstract import AbstractOptimize
from SplineOptimization.periodic_fun import period_splines, not_period_splines


class SplineOptimize(AbstractOptimize):
    def __init__(self, task):
        super().__init__(task=task)

        self.knots_number = task["SPL"]["knots_number"]
        self.number_of_shapes = task["SPL"]["number_of_shapes"]
        self.colors_of_shapes = {phase: color for phase, color in self.colors.items() if
                                 phase != self.background_color_key}
        self.color_and_activation_range = len(self.colors_of_shapes)
        self.grid_size = calc_grid_size(self.number_of_shapes)
        self.extra_bounding_dist = self.calc_shapes_range_dist()
        self.activation_number = task["job"]["activation_value"] * self.color_and_activation_range
        self.periodic_type_f = period_splines if task["SPL"]["periodic"] else not_period_splines
        self.splines_dpi = 100 if self.periodic_type_f.__name__ == "not_period_splines" else 420

    def calc_shapes_range_dist(self):
        extra_range = [0, 0]  # [math.floor(dist[0]/4),math.floor(dist[1]/4)] # not necessary
        dist = [math.floor(self.x_size / (2 * self.grid_size[0])) + extra_range[0],
                math.floor(self.y_size / (2 * self.grid_size[1])) + extra_range[1]]
        return dist

    def generate_pt(self, random, args):
        shapes_range = []
        for shape_nr in range(self.number_of_shapes):
            # full random center point of shape
            x_center = randrange(0, self.x_size)
            y_center = randrange(0, self.y_size)
            x_dist = randrange(round(self.extra_bounding_dist[0] / 2), round(1.5 * self.extra_bounding_dist[0]))
            y_dist = randrange(round(self.extra_bounding_dist[1] / 2), round(1.5 * self.extra_bounding_dist[1]))
            r = {"x": [x_center - x_dist,
                       x_center + x_dist],
                 "y": [y_center - y_dist,
                       y_center + y_dist]}
            shapes_range.append(r)
        shapes = []

        for shape in shapes_range:
            for knot_number in range(self.knots_number):
                shapes.append(uniform(shape["x"][0], shape["x"][1]))
                shapes.append(uniform(shape["y"][0], shape["y"][1]))
                shapes.append(uniform(0, self.color_and_activation_range))  # activation value of point

        shapes.extend(
            [uniform(0, self.color_and_activation_range) for _ in range(len(shapes_range))])  # color for shape
        return shapes

    def bound_pt(self, candidate, args):

        for i in range(self.number_of_shapes * self.knots_number):
            candidate[i * 3] = max(min(candidate[i * 3], self.x_size + 2 * self.extra_bounding_dist[0]),
                                   - 2 * self.extra_bounding_dist[0])
            candidate[i * 3 + 1] = max(min(candidate[i * 3 + 1], self.y_size + 2 * self.extra_bounding_dist[1]),
                                       - 2 * self.extra_bounding_dist[1])
            candidate[i * 3 + 2] = max(min(candidate[i * 3 + 2], self.color_and_activation_range), 0)  # activation

        cl = len(candidate)
        for i in range(cl - self.number_of_shapes, cl):
            candidate[i] = max(min(candidate[i], self.color_and_activation_range), 0)
        return candidate

    def create_starting_points_from_candidate(self, candidate):
        """
        Zwraca listę list punktów węzłowych [x,y]
        :param candidate:
        :return:
        """
        curves = list(candidate)
        curves = curves[: - self.number_of_shapes]
        curves = [curves[i:i + 3] for i in range(0, len(curves), 3)]
        curves = [curves[i:i + self.knots_number] for i in range(0, len(curves), self.knots_number)]
        curves = [[[round(point[0]), round(point[1])] for point in curve if point[2] > self.activation_number] for curve
                  in curves]
        colors_list = candidate[-self.number_of_shapes:]

        end_colors_list = []
        end_curves = []
        for color, curve in zip(colors_list, curves):
            if len(curve) > 2:
                end_colors_list.append(color)
                end_curves.append(curve)
        shapes_colors = indexes_to_rgb(self.colors_of_shapes, end_colors_list)
        return end_curves, shapes_colors

    def create_ssrve_image(self, args):
        return create_ssrve_image(*args, background_color=self.background_color, x_size=self.x_size, y_size=self.y_size,
                                  periodic_type_f=self.periodic_type_f, splines_dpi=self.splines_dpi)

    def calc_candidate_fitness(self, candidate):
        return super().calc_candidate_fitness(candidate)

    def evaluate_pt(self, candidates, args):
        return super().evaluate_pt(candidates, args)

    def ssrve_observer(self, population, num_generations, num_evaluations, args):
        return super().ssrve_observer(population, num_generations, num_evaluations, args)

    def optimize(self):
        super().optimize()

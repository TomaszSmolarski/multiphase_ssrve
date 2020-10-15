# -*- coding: utf-8 -*-

import math
from random import randrange
from SplineOptimization.shapes_fun import calc_grid_size, indexes_to_rgb, list_of_shapes_colors
from SplineOptimization.ssrve_fun import create_ssrve_image
from default_config import d_threads, d_colors, d_x_size, d_y_size, d_knots_number, d_pop_size, d_ratios
from optimization_abstract import AbstractOptimize


class SplineOptimize(AbstractOptimize):
    def __init__(self, picture_path, periodic_type_f, threads=d_threads, colors=d_colors, x_size=d_x_size,
                 y_size=d_y_size,
                 knots_number=d_knots_number, pop_size=d_pop_size, ratios=d_ratios, ):
        super().__init__(picture_path=picture_path, threads=threads, colors=colors,
                         x_size=x_size, y_size=y_size, pop_size=pop_size, ratios=ratios)

        self.knots_number = knots_number
        self.shapes_colors = list_of_shapes_colors(self.ratios, self.colors, self.target_series_from_ratios)
        self.number_of_shapes = len(self.shapes_colors)
        self.grid_size = calc_grid_size(self.number_of_shapes)
        self.shapes_range = self.generate_shapes_range()
        self.activation_number = 30
        self.periodic_type_f = periodic_type_f

    def generate_shapes_range(self):
        dist = [math.floor(self.x_size / self.grid_size[0]), math.floor(self.y_size / self.grid_size[1])]
        extra_range = [0, 0]  # [math.floor(dist[0]/4),math.floor(dist[1]/4)] # not necessary
        shapes_range = []
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                if self.grid_size[1] * row + col >= self.number_of_shapes:
                    break
                r = {"x": [row * dist[0] - extra_range[0], (row + 1) * dist[0] + extra_range[0]],
                     "y": [col * dist[1] - extra_range[1], (col + 1) * dist[1] + extra_range[0]]}
                shapes_range.append(r)

        return shapes_range

    def generate_pt(self, random, args):
        shapes = []
        for shape in self.shapes_range:
            for knot_number in range(self.knots_number):
                # shapes.append(randrange(0, self.x_size))
                # shapes.append(randrange(0, self.y_size))
                shapes.append(randrange(shape["x"][0], shape["x"][1]))
                shapes.append(randrange(shape["y"][0], shape["y"][1]))
                shapes.append(randrange(0, 100))  # activation value of point
        shapes.extend(random.sample(self.shapes_colors, len(self.shapes_colors)))

        return shapes

    def bound_pt(self, candidate, args):
        for i in range(self.number_of_shapes * self.knots_number):
            candidate[i * 3] = max(min(candidate[i * 3], self.x_size - 1), 0)
            candidate[i * 3 + 1] = max(min(candidate[i * 3 + 1], self.y_size - 1), 0)
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
        curves = [[[point[0], point[1]] for point in curve if point[2] > self.activation_number] for curve in curves]
        curves = [curve for curve in curves if len(curve) > 2]

        shapes_colors = indexes_to_rgb(self.colors, shapes_colors_list)
        return curves, shapes_colors

    def create_ssrve_image(self,args):
        return create_ssrve_image(*args, background_color=self.background_color,x_size=self.x_size, y_size=self.y_size,
                                  periodic_type_f=self.periodic_type_f)

    def calc_candidate_fitness(self, starting_points):
        return super().calc_candidate_fitness(starting_points)

    def evaluate_pt(self, candidates, args):
        return super().evaluate_pt(candidates, args)

    def ssrve_observer(self, population, num_generations, num_evaluations, args):
        return super().ssrve_observer(population, num_generations, num_evaluations, args)

    def optimize(self):
        super().optimize()

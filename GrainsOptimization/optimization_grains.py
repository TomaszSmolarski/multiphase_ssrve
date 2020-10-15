# -*- coding: utf-8 -*-


from random import randrange
from GrainsOptimization.grain_grown import create_ssrve_image
from default_config import d_threads, d_colors, d_x_size, \
    d_y_size, d_starting_points_number, d_pop_size, d_ratios
from optimization_abstract import AbstractOptimize


class GrainOptimize(AbstractOptimize):
    def __init__(self, picture_path, threads=d_threads, colors=d_colors, x_size=d_x_size, y_size=d_y_size,
                 starting_points_number=d_starting_points_number, pop_size=d_pop_size, ratios=d_ratios):

        super().__init__(picture_path=picture_path, threads=threads, colors=colors,
                         x_size=x_size, y_size=y_size, pop_size=pop_size, ratios=ratios)
        self.starting_points_number = starting_points_number
        self.colors_bgr_list = [(item[2], item[1], item[0]) for key, item in self.colors.items()]
        self.colors_weights = [weight for weight in self.target_stats['onePointprobability'].values()]

    def generate_pt(self, random, args):
        points = []
        for nr in range(self.starting_points_number):
            points.append(randrange(0, self.x_size))  # x
            points.append(randrange(0, self.y_size))  # y
            color_index = random.choices(range(0, self.colors_len), weights=self.colors_weights, k=1)
            points.append(color_index[0])  # color

        return points

    def bound_pt(self, candidate, args):
        for i in range(self.starting_points_number):
            candidate[i * 3] = max(min(candidate[i * 3], self.x_size - 1), 0)
            candidate[i * 3 + 1] = max(min(candidate[i * 3 + 1], self.y_size - 1), 0)
            candidate[i * 3 + 2] = max(min(candidate[i * 3 + 2], self.colors_len - 1), 0)
        return candidate

    def create_starting_points_from_candidate(self, candidate):
        """
        Zwraca listę tupli punktów startowych (x,y,c)
        :param candidate:
        :return:candidate[i:i + 3]
        """
        pts = [tuple([round(candidate[i]) % self.x_size,
                      round(candidate[i + 1]) % self.y_size,
                      round(candidate[i + 2]) % self.colors_len]) for i in range(0, len(candidate), 3)]
        return [pts] # Because args are tuple and i want to have list of points I have to pack this list with []

    def create_ssrve_image(self,args):
        return create_ssrve_image(*args, height=self.y_size, width=self.x_size, colors_bgr_list=self.colors_bgr_list)

    def calc_candidate_fitness(self, starting_points):
        return super().calc_candidate_fitness(starting_points)

    def ssrve_observer(self, population, num_generations, num_evaluations, args):
        return super().ssrve_observer(population, num_generations, num_evaluations, args)

    def evaluate_pt(self, candidates, args):
        return super().evaluate_pt(candidates, args)

    def optimize(self):
        return super().optimize()

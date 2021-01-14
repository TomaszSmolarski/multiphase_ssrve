# -*- coding: utf-8 -*-


import random
from GrainsOptimization.grain_growth import GrainGrowth
from optimization_abstract import AbstractOptimize


class GrainOptimize(AbstractOptimize):
    def __init__(self, task):
        super().__init__(task=task)
        self.starting_points_number = task["GR"]["starting_points_number"]
        self.colors_bgr_list = [(item[2], item[1], item[0]) for key, item in self.colors.items()]
        self.grain_growth = GrainGrowth(height=self.y_size, width=self.x_size,
                                        colors_bgr_list=self.colors_bgr_list,
                                        periodic=True if task["GR"]["periodic"] else False)
        self.colors_len = len(list(self.colors.values()))

    def generate_pt(self, random, args):
        points = []
        for nr in range(self.starting_points_number):
            points.append(random.uniform(0, self.x_size))  # x
            points.append(random.uniform(0, self.y_size))  # y
            points.append(random.uniform(0, self.colors_len))  # color

        return points

    def bound_pt(self, candidate, args):
        for i in range(self.starting_points_number):
            candidate[i * 3] = max(min(candidate[i * 3], self.x_size - 1), 0)
            candidate[i * 3 + 1] = max(min(candidate[i * 3 + 1], self.y_size - 1), 0)
            candidate[i * 3 + 2] = max(min(candidate[i * 3 + 2], self.colors_len), 0)
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
        return [pts]  # Because args are tuple and i want to have list of points I have to pack this list with []

    def create_ssrve_image(self, args):
        return self.grain_growth.create_ssrve_image(*args)

    def calc_candidate_fitness(self, candidate):
        return super().calc_candidate_fitness(candidate)

    def ssrve_observer(self, population, num_generations, num_evaluations, args):
        return super().ssrve_observer(population, num_generations, num_evaluations, args)

    def evaluate_pt(self, candidates, args):
        return super().evaluate_pt(candidates, args)

    def optimize(self):
        return super().optimize()

# -*- coding: utf-8 -*-

import math
from datetime import timedelta
from random import Random, randrange
from time import time
from multiprocessing import Pool
import fitness_fun
import cv2
import inspyred
from GrainsSeeker.main import mainFunction
from ssrve_fun import create_ssrve_image, save_to_file, calc_grid_size, list_of_shapes_colors, indexes_to_rgb


class Optimize:
    def __init__(self, picture_path, threads=4, colors=None, x_size=300, y_size=200,
                 knots_number=16, pop_size=20, ratios=None):
        super().__init__()
        self.target_series_from_ratios = {}
        self.target_stats = {}
        self.picture_path = picture_path
        if colors is None:
            colors = {'ferrite': (29, 143, 255),
                      'bainite': (172, 255, 46),
                      'martensite': (255, 0, 0)}

        if ratios is None:
            ratios = ['Malinowska',
                      'Blair Bliss',
                      'Danielsson',
                      'Haralick',
                      'Mz',
                      'RLS',
                      'RF',
                      'RC1',
                      'RC2',
                      'RCOM',
                      'LP1',
                      'LP2',
                      'LP3']
        self.ratios = ratios
        self.colors = colors
        self.background_color = list(self.colors.values())[-1]
        self.background_color_key = list(self.colors.keys())[-1]
        self.x_size = x_size
        self.y_size = y_size
        self.knots_number = knots_number
        self.threads = threads
        self.start_time = time()
        self.pop_size = pop_size
        self.shapes_colors = self.generate_shapes_colors()
        self.number_of_shapes = len(self.shapes_colors)
        self.grid_size = calc_grid_size(self.number_of_shapes)
        self.shapes_range = self.generate_shapes_range()
        self.activation_number = 30

    def generate_shapes_colors(self):
        image = cv2.imread(self.picture_path)
        seriesFromRatios, stats = mainFunction(image, ratios=self.ratios, colors=self.colors,
                                               background=self.background_color_key)
        self.target_series_from_ratios = seriesFromRatios
        self.target_stats = stats

        list_of_colors, indexes = list_of_shapes_colors(self.ratios, self.colors, seriesFromRatios)
        return indexes

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
                shapes.append(randrange(0, self.x_size))
                shapes.append(randrange(0, self.y_size))
                #shapes.append(randrange(shape["x"][0], shape["x"][1]))
                #shapes.append(randrange(shape["y"][0], shape["y"][1]))
                shapes.append(randrange(0,100)) #activation value of point
        shapes.extend(random.sample(self.shapes_colors, len(self.shapes_colors)))
        return shapes

    def bound_pt(self, candidate, args):
        for i in range(self.number_of_shapes * self.knots_number):
            #candidate[i * 2] = max(min(candidate[i * 2], self.x_size - 1), 0)
            #candidate[i * 2 + 1] = max(min(candidate[i * 2 + 1], self.y_size - 1), 0)
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
        curves = [[[point[0],point[1]] for point in curve if point[2]>self.activation_number] for curve in curves]
        curves = [curve for curve in curves if len(curve)>2]

        shapes_colors = indexes_to_rgb(self.colors, shapes_colors_list)
        return curves, shapes_colors

    def calc_candidate_fitness(self, starting_points):
        """
        Zwraca wartosc przystosowania elementu SSRVE zadanego zbiorem punktow startowych
        :param starting_points: lista list określających punkty węzłowy [x,y]
        :return: Wartość przystosowania w zakresie float <0, 1>
        """
        curves, shapes_colors = self.create_starting_points_from_candidate(starting_points)

        img = create_ssrve_image(curves, shapes_colors=shapes_colors, background_color=self.background_color
                                 , x_size=self.x_size, y_size=self.y_size)
        #save_to_file('test{}.png'.format(shapes_index), img)
        series_from_ratios, stats = mainFunction(img, ratios=self.ratios, colors=self.colors,
                                                 background=self.background_color_key)

        # Blad sredniokwadratowy dla danego osobnika
        candidate_fitness = fitness_fun.candidate_fitness(series_from_ratios, stats,
                                                          self.target_series_from_ratios, self.target_stats)
        print(series_from_ratios, stats, candidate_fitness, sep="---")
        return candidate_fitness

    def evaluate_pt(self, candidates, args):
        dataset = []

        for nr, candidate in enumerate(candidates):
            dataset.append(candidate)

        chunk_size = 1
        with Pool(processes=self.threads) as pool:
            fitness = pool.map(self.calc_candidate_fitness, dataset, chunk_size)
        return fitness

    def ssrve_observer(self, population, num_generations, num_evaluations, args):

        population_copy = population.copy()
        population_copy.sort(reverse=True)
        best = population_copy[0].candidate
        curves, shapes_colors = self.create_starting_points_from_candidate(best)
        img = create_ssrve_image(curves, shapes_colors=shapes_colors, background_color=self.background_color,
                                 x_size=self.x_size, y_size=self.y_size)
        save_to_file('Results/BEST_IN_{0}_POPULATION.png'.format(num_generations), img)

    def time_observer(self, population, num_generations, num_evaluations, args):
        elapsed = time() - self.start_time
        print("--- Evaluation of generation {0} took {1} ---".format(num_generations, str(timedelta(seconds=elapsed))))
        self.start_time = time()

    def optimize(self):
        prng = Random()
        prng.seed(time())
        '''
        ea = inspyred.ec.GA(prng)
        ea.observer = [inspyred.ec.observers.file_observer, inspyred.ec.observers.stats_observer,
                       self.ssrve_observer, self.time_observer]
        ea.selector = inspyred.ec.selectors.rank_selection
        ea.variator = [inspyred.ec.variators.blend_crossover, inspyred.ec.variators.gaussian_mutation]
        ea.replacer = inspyred.ec.replacers.crowding_replacement
        ea.terminator = [
            inspyred.ec.terminators.no_improvement_termination,
            inspyred.ec.terminators.diversity_termination,
            inspyred.ec.terminators.user_termination
        ]
        final_pop = ea.evolve(generator=self.generate_pt,
                              evaluator=self.evaluate_pt,
                              pop_size=self.pop_size,  # default 100
                              maximize=False,
                              bounder=self.bound_pt,
                              max_evaluations=1000,
                              statistics_file=open("stats.csv", "w"),
                              individuals_file=open("individuals.csv", "w"),
                              mutation_rate=0.25,  # default 0.1
                              num_crossover_points=4,  # default 1
                              crossover_rate=0.2,  # default 0.1
                              num_selected=20,  # default len(population)
                            
                              )
        '''

        ea = inspyred.swarm.PSO(prng)
        ea.observer = [inspyred.ec.observers.file_observer, inspyred.ec.observers.stats_observer, self.ssrve_observer,
                       self.time_observer]
        ea.terminator = [inspyred.ec.terminators.evaluation_termination,
                         inspyred.ec.terminators.average_fitness_termination]

        ea.topology = inspyred.swarm.topologies.star_topology  # or ring_topology, star better
        final_pop = ea.evolve(generator=self.generate_pt,
                              evaluator=self.evaluate_pt,
                              pop_size=self.pop_size,
                              bounder=self.bound_pt,
                              maximize=False,
                              statistics_file=open("stats.csv", "w"),
                              individuals_file=open("individuals.csv", "w"),
                              max_evaluations=1000,
                              neighborhood_size=3,
                              inertia=0.5,  # default 0.5
                              cognitive_rate=1.4,  # default 2.1
                              social_rate=1.4,  # default 2.1
                              )

        # inspyred.ec.analysis.generation_plot(open("stats.csv", "r"))
        # inspyred.ec.analysis.allele_plot("individuals.csv")

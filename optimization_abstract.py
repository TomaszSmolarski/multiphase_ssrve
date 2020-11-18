import csv
import math
import operator
from abc import ABC, abstractmethod
from multiprocessing import Pool
from random import Random
import cv2
import inspyred
from datetime import timedelta
from GrainsSeeker.main import mainFunction
from time import time

from SplineOptimization.shapes_fun import rgb2hex
from SplineOptimization.ssrve_fun import save_to_file
from fitness_fun import calculate_candidate_mean_square_error
from statistics import median
from copy import deepcopy


class AbstractOptimize(ABC):
    def __init__(self, picture_path, threads, colors, x_size, y_size,
                 pop_size, ratios, ratios_periodic, save_dir_path, target_series_from_ratios, target_stats):
        super().__init__()
        self.picture_path = picture_path
        self.ratios = ratios
        self.colors = colors
        self.colors_len = len(list(self.colors.values()))
        self.x_size = x_size
        self.y_size = y_size
        self.save_dir_path = save_dir_path
        self.background_color = rgb2hex(*list(self.colors.values())[-1])
        self.background_color_key = list(self.colors.keys())[-1]
        self.threads = threads
        self.pop_size = pop_size
        self.start_time = time()
        self.ratios_periodic = ratios_periodic
        self.target_series_from_ratios, self.target_stats = target_series_from_ratios, target_stats
        self.target_series_from_ratios_median = self.target_calc()
        self.times_array = []

    def time_observer(self, population, num_generations, num_evaluations, args):
        elapsed = time() - self.start_time
        print("--- Evaluation of generation {0} took {1} ---".format(num_generations, str(timedelta(seconds=elapsed))))
        self.times_array.append([num_generations, timedelta(seconds=elapsed)])
        self.start_time = time()

    def target_calc(self):
        if not (self.target_series_from_ratios and self.target_stats):
            image = cv2.imread(self.picture_path)
            self.target_series_from_ratios, self.target_stats = mainFunction(image, ratios=self.ratios,
                                                                             colors=self.colors,
                                                                             periodical=self.ratios_periodic)
        new_background_color = max(self.target_stats['onePointprobability'].items(), key=operator.itemgetter(1))[0]
        if new_background_color != self.background_color_key:
            self.background_color_key = new_background_color
            self.background_color = rgb2hex(*list(self.colors[new_background_color]))

        self.target_series_from_ratios[self.background_color_key] = {}

        target_series_from_ratios_median = deepcopy(self.target_series_from_ratios)
        for phase, ratios in target_series_from_ratios_median.items():
            for ratio_name, values in ratios.items():
                ratios[ratio_name] = median(list(values.values()))

        print(self.target_series_from_ratios, self.target_stats)
        print(target_series_from_ratios_median)
        return target_series_from_ratios_median

    def save_relative_errors_to_file(self, candidate, num_generations):
        # Zapisz naglowki
        if num_generations == 0:
            header = ''
            if self.ratios:
                for phase, ratios in self.target_series_from_ratios_median.items():
                    for ratio_name in ratios.keys():
                        header += "{0}/{1},".format(phase, ratio_name)

            for stat, ratios in self.target_stats.items():
                for ratio_name in ratios.keys():
                    header += "{0}/{1},".format(stat, ratio_name)

            with open(self.save_dir_path+'relative_errors.csv', 'w') as f:
                f.write('{}\n'.format(header[:-1]))             # [:-1] pomija ostatni przecinek
            return
        args = (self.create_starting_points_from_candidate(candidate))
        img = self.create_ssrve_image(args)

        # Zapisz dane
        data_str = ''
        ratios, stats = mainFunction(img, ratios=self.ratios, colors=self.colors, periodical=self.ratios_periodic)

        for tr, r in zip(self.target_series_from_ratios_median.values(), ratios.values()):
            for target_ratio, ssrve_ratio_dict in zip(tr.values(), r.values()):
                ssrve_ratio = median(list(ssrve_ratio_dict.values()))
                relative_err = math.fabs((target_ratio - ssrve_ratio) / target_ratio)
                data_str += "{0:.3f},".format(relative_err)

        for ts, s in zip(self.target_stats.values(), stats.values()):
            for target_stat, ssrve_stat in zip(ts.values(), s.values()):
                relative_err = math.fabs((target_stat - ssrve_stat) / target_stat)
                data_str += "{0:.3f},".format(relative_err)

        with open(self.save_dir_path+'relative_errors.csv', 'a+') as f:
            f.write('{}\n'.format(data_str[:-1]))               # [:-1] pomija ostatni przecinek

    def coefficients_observer(self, population, num_generations, num_evaluations, args):
        population_copy = population.copy()
        population_copy.sort(reverse=True)
        best = population_copy[0].candidate
        self.save_relative_errors_to_file(best, num_generations)

    @abstractmethod
    def evaluate_pt(self, candidates, args):
        dataset = []
        for candidate in candidates:
            dataset.append(candidate)
        chunk_size = 1
        with Pool(processes=self.threads) as pool:
            fitness = pool.map(self.calc_candidate_fitness, dataset, chunk_size)
        return fitness

    @abstractmethod
    def generate_pt(self, random, args):
        raise NotImplementedError("Subclasses should implement this!")

    @abstractmethod
    def bound_pt(self, candidate, args):
        raise NotImplementedError("Subclasses should implement this!")

    @abstractmethod
    def create_starting_points_from_candidate(self, candidate):
        raise NotImplementedError("Subclasses should implement this!")

    @abstractmethod
    def create_ssrve_image(self, kwargs):
        raise NotImplementedError("Subclasses should implement this!")

    @abstractmethod
    def calc_candidate_fitness(self, candidate):
        """
        Zwraca wartosc przystosowania elementu SSRVE zadanego zbiorem punktow startowych
        :return: Wartość przystosowania w zakresie float <0, 1>
        """
        args = (self.create_starting_points_from_candidate(candidate))
        img = self.create_ssrve_image(args)
        series_from_ratios, stats = mainFunction(img, ratios=self.ratios, colors=self.colors,
                                                 background=self.background_color_key, periodical=self.ratios_periodic)
        # Blad sredniokwadratowy dla danego osobnika
        candidate_fitness = calculate_candidate_mean_square_error(series_from_ratios, stats,
                                                                  self.target_series_from_ratios,
                                                                  self.target_stats)
        print(series_from_ratios, stats, candidate_fitness, sep="---")
        return candidate_fitness

    @abstractmethod
    def ssrve_observer(self, population, num_generations, num_evaluations, args):
        population_copy = population.copy()
        population_copy.sort(reverse=True)
        best = population_copy[0].candidate
        args = (self.create_starting_points_from_candidate(best))
        img = self.create_ssrve_image(args)
        save_to_file(self.save_dir_path + 'Results/BEST_IN_{0}_POPULATION.png'.format(num_generations), img)

    @abstractmethod
    def optimize(self):
        prng = Random()
        seed = time()  # 1234567
        prng.seed(seed)

        ea = inspyred.ec.DEA(prng)
        ea.observer = [inspyred.ec.observers.file_observer, inspyred.ec.observers.stats_observer,
                       self.ssrve_observer, self.time_observer, self.coefficients_observer]
        ea.selector = inspyred.ec.selectors.tournament_selection
        # ea.selector = inspyred.ec.selectors.truncation_selection
        # ea.selector = inspyred.ec.selectors.rank_selection
        ea.variator = [inspyred.ec.variators.blend_crossover, inspyred.ec.variators.gaussian_mutation]

        ea.replacer = inspyred.ec.replacers.truncation_replacement
        # ea.replacer = inspyred.ec.replacers.crowding_replacement

        ea.terminator = [
            inspyred.ec.terminators.no_improvement_termination,
            inspyred.ec.terminators.evaluation_termination,

            inspyred.ec.terminators.user_termination
        ]#inspyred.ec.terminators.diversity_termination,
        final_pop = ea.evolve(generator=self.generate_pt,
                              evaluator=self.evaluate_pt,
                              pop_size=self.pop_size,
                              bounder=self.bound_pt,
                              maximize=False,
                              max_evaluations=1000,
                              num_selected=self.pop_size,
                              tournament_size=2,  # 2 best
                              crossover_rate=0.2,  # 0.2 best
                              num_crossover_points=1,
                              mutation_rate=0.285,  # 0.285 best
                              gaussian_mean=0,
                              gaussian_stdev=1,
                              statistics_file=open(self.save_dir_path + "stats.csv", "w"),
                              individuals_file=open(self.save_dir_path + "individuals.csv", "w"),

                              )

        '''
        ea = inspyred.swarm.PSO(prng) #nope for splines
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
                              statistics_file=open(self.save_dir_path + "stats.csv", "w"),
                              individuals_file=open(self.save_dir_path + "individuals.csv", "w"),
                              max_evaluations=1000,
                              neighborhood_size=3,
                              inertia=0.5,  # default 0.5
                              cognitive_rate=1.4,  # default 2.1
                              social_rate=1.4,  # default 2.1
                              )
        '''

        times_sum = sum([sec[1] for sec in self.times_array], timedelta())
        csvfile = open(self.save_dir_path + 'times.csv', 'w', newline='')
        writer = csv.writer(csvfile)
        writer.writerows(self.times_array)
        writer.writerow(["sum/avg", times_sum, times_sum / len(self.times_array)])
        for nr, c in enumerate(final_pop):
            print(c)
            writer.writerow([nr, c])

        # inspyred.ec.analysis.generation_plot(open("stats.csv", "r"))
        # inspyred.ec.analysis.allele_plot("individuals.csv")

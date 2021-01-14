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
from statistics import median
from copy import deepcopy
from default_config import ratios_weights


class AbstractOptimize(ABC):
    def __init__(self, task):
        super().__init__()
        self.picture_path = task["picture_path"]
        self.ratios = task["job"]["ratios"]
        self.colors = task["job"]["colors"]
        self.x_size = task["job"]["x_size"]
        self.y_size = task["job"]["y_size"]
        self.save_dir_path = task["job"]["save_dir_path"]
        self._background_color = self.rgb2hex(*list(self.colors.values())[-1])
        self._background_color_key = list(self.colors.keys())[-1]
        self.threads = task["job"]["threads"]
        self.pop_size = task["job"]["pop_size"]
        self.__start_time = time()
        self.ratios_periodic = task["job"]["ratios_periodic"]
        self.target_series_from_ratios, self.target_stats = task["target_series_from_ratios"], task["target_stats"]
        self.target_series_from_ratios_median = self.target_calc()
        self.times_array = []
        self.task = task

    def time_observer(self, population, num_generations, num_evaluations, args):
        elapsed = time() - self.__start_time
        print("--- Evaluation of generation {0} took {1} ---".format(num_generations, str(timedelta(seconds=elapsed))))
        self.times_array.append([num_generations, timedelta(seconds=elapsed)])
        self.__start_time = time()

    @staticmethod
    def rgb2hex(r, g, b):
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    @staticmethod
    def save_to_file(file_path, image_open_cv):
        try:
            cv2.imwrite(file_path, img=image_open_cv)
        except:
            print('first render file')

    def target_calc(self):
        if not (self.target_series_from_ratios and self.target_stats):
            image = cv2.imread(self.picture_path)
            self.target_series_from_ratios, self.target_stats = mainFunction(image, ratios=self.ratios,
                                                                             colors=self.colors,
                                                                             periodical=self.ratios_periodic)
        new_background_color = max(self.target_stats['onePointprobability'].items(), key=operator.itemgetter(1))[0]
        if new_background_color != self._background_color_key:
            self._background_color_key = new_background_color
            self._background_color = self.rgb2hex(*list(self.colors[new_background_color]))

        self.target_series_from_ratios[self._background_color_key] = {}

        target_series_from_ratios_median = deepcopy(self.target_series_from_ratios)
        for phase, ratios in target_series_from_ratios_median.items():
            for ratio_name, values in ratios.items():
                ratios[ratio_name] = median(list(values.values()))

        print(target_series_from_ratios_median, self.target_stats)
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

            with open(self.save_dir_path + 'relative_errors.csv', 'w') as f:
                f.write('{}\n'.format(header[:-1]))  # [:-1] pomija ostatni przecinek
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

        with open(self.save_dir_path + 'relative_errors.csv', 'a+') as f:
            f.write('{}\n'.format(data_str[:-1]))  # [:-1] pomija ostatni przecinek

    def calculate_candidate_mean_square_error(self, series_from_ratios, stats):
        x = 0
        number_of_coefficients = 0
        stats_weight = 1
        for target_phase_params, test_phase_params in zip(self.target_series_from_ratios.values(),
                                                          series_from_ratios.values()):
            for target_ratios, test_ratios in zip(target_phase_params.items(), test_phase_params.items()):
                if target_ratios[1]:
                    target_ratios_median = median(list(target_ratios[1].values()))
                else:
                    target_ratios_median = 0
                if test_ratios[1]:
                    test_ratios_median = median(list(test_ratios[1].values()))
                else:
                    test_ratios_median = 1
                x += ratios_weights[target_ratios[0]] * pow(test_ratios_median - target_ratios_median, 2)

        for target_stats_elem, test_stats_elem in zip(self.target_stats.values(), stats.values()):
            for target_stats, test_stats in zip(list(target_stats_elem.values()), list(test_stats_elem.values())):
                x += stats_weight * pow(test_stats - target_stats, 2)
                number_of_coefficients += 1
        return (1 / number_of_coefficients) * math.sqrt(x)

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
                                                 background=self._background_color_key, periodical=self.ratios_periodic)
        # Blad sredniokwadratowy dla danego osobnika
        candidate_fitness = self.calculate_candidate_mean_square_error(series_from_ratios, stats)
        print(series_from_ratios, stats, candidate_fitness, sep="---")
        return candidate_fitness

    @abstractmethod
    def ssrve_observer(self, population, num_generations, num_evaluations, args):
        population_copy = population.copy()
        population_copy.sort(reverse=True)
        best = population_copy[0].candidate
        args = (self.create_starting_points_from_candidate(best))
        img = self.create_ssrve_image(args)
        self.save_to_file(self.save_dir_path + 'Results/BEST_IN_{0}_POPULATION.png'.format(num_generations), img)

    @abstractmethod
    def optimize(self):
        prng = Random()
        seed = time()  # 1234567
        prng.seed(seed)

        if self.task["optimization_method"] == "DEA":
            ea = inspyred.ec.DEA(prng)
            ea.observer = [inspyred.ec.observers.file_observer, inspyred.ec.observers.stats_observer,
                           self.ssrve_observer, self.time_observer, self.coefficients_observer]
            ea.selector = inspyred.ec.selectors.tournament_selection
            ea.variator = [inspyred.ec.variators.blend_crossover, inspyred.ec.variators.gaussian_mutation]
            ea.replacer = inspyred.ec.replacers.truncation_replacement

            ea.terminator = [
                inspyred.ec.terminators.generation_termination
            ]  # inspyred.ec.terminators.diversity_termination,
            # inspyred.ec.terminators.no_improvement_termination,
            # inspyred.ec.terminators.evaluation_termination,
            final_pop = ea.evolve(generator=self.generate_pt,
                                  evaluator=self.evaluate_pt,
                                  pop_size=self.pop_size,
                                  bounder=self.bound_pt,
                                  maximize=False,
                                  max_evaluations=self.task["job"]["max_evaluations"],
                                  max_generations=self.task["job"]["max_generations"],
                                  num_selected=self.pop_size,
                                  tournament_size=self.task["DEA"]["tournament_size"],  # 2 best
                                  crossover_rate=self.task["DEA"]["crossover_rate"],  # 0.2 best
                                  num_crossover_points=self.task["DEA"]["num_crossover_points"],
                                  mutation_rate=self.task["DEA"]["mutation_rate"],  # 0.285 best
                                  gaussian_mean=self.task["DEA"]["gaussian_mean"],
                                  gaussian_stdev=self.task["DEA"]["gaussian_stdev"],
                                  statistics_file=open(self.save_dir_path + "stats.csv", "w"),
                                  individuals_file=open(self.save_dir_path + "individuals.csv", "w"),
                                  )
        elif self.task["optimization_method"] == "PSO":
            ea = inspyred.swarm.PSO(prng)
            ea.observer = [inspyred.ec.observers.file_observer, inspyred.ec.observers.stats_observer,
                           self.ssrve_observer,
                           self.time_observer, self.coefficients_observer]
            ea.terminator = [inspyred.ec.terminators.generation_termination]
            # inspyred.ec.terminators.evaluation_termination
            # inspyred.ec.terminators.average_fitness_termination
            ea.topology = inspyred.swarm.topologies.star_topology  # or ring_topology, star better
            final_pop = ea.evolve(generator=self.generate_pt,
                                  evaluator=self.evaluate_pt,
                                  pop_size=self.pop_size,
                                  bounder=self.bound_pt,
                                  maximize=False,
                                  statistics_file=open(self.save_dir_path + "stats.csv", "w"),
                                  individuals_file=open(self.save_dir_path + "individuals.csv", "w"),
                                  max_evaluations=self.task["job"]["max_evaluations"],
                                  max_generations=self.task["job"]["max_generations"],
                                  inertia=self.task["PSO"]["inertia"],  # default 0.5
                                  cognitive_rate=self.task["PSO"]["cognitive_rate"],  # default 2.1
                                  social_rate=self.task["PSO"]["social_rate"],  # default 2.1
                                  )
        else:
            raise Exception('Optimization method should be PSO or DEA not: {}. Check task in default_config.py file'
                            .format(self.task["optimization_method"]))

        times_sum = sum([sec[1] for sec in self.times_array], timedelta())
        csvfile = open(self.save_dir_path + 'times.csv', 'w', newline='')
        writer = csv.writer(csvfile)
        writer.writerows(self.times_array)
        writer.writerow(["sum/avg", times_sum, times_sum / len(self.times_array)])
        writer.writerow(["seed", seed])
        for nr, c in enumerate(final_pop):
            print(c)
            writer.writerow([nr, c])

        # inspyred.ec.analysis.generation_plot(open("stats.csv", "r"))
        # inspyred.ec.analysis.allele_plot("individuals.csv")

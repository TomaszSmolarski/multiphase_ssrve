from abc import ABC, abstractmethod
from multiprocessing import Pool
from random import Random
import cv2
import inspyred
from datetime import timedelta
from GrainsSeeker.main import mainFunction
from time import time

from SplineOptimization.ssrve_fun import save_to_file
from fitness_fun import calculate_candidate_mean_square_error


class AbstractOptimize(ABC):
    def __init__(self, picture_path, threads, colors, x_size, y_size,
                 pop_size, ratios):
        super().__init__()
        self.picture_path = picture_path
        self.ratios = ratios
        self.colors = colors
        self.background_color = list(self.colors.values())[-1]
        self.background_color_key = list(self.colors.keys())[-1]
        self.colors_len = len(list(self.colors.values()))
        self.x_size = x_size
        self.y_size = y_size
        self.threads = threads
        self.pop_size = pop_size
        self.start_time = time()
        self.target_series_from_ratios, self.target_stats = self.target_calc()

    def time_observer(self, population, num_generations, num_evaluations, args):
        elapsed = time() - self.start_time
        print("--- Evaluation of generation {0} took {1} ---".format(num_generations, str(timedelta(seconds=elapsed))))
        self.start_time = time()

    def target_calc(self):
        image = cv2.imread(self.picture_path)
        seriesFromRatios, stats = mainFunction(image, ratios=self.ratios, colors=self.colors,
                                               background=self.background_color_key)
        return seriesFromRatios, stats

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
    def create_ssrve_image(self,kwargs):
        raise NotImplementedError("Subclasses should implement this!")

    @abstractmethod
    def calc_candidate_fitness(self, starting_points):
        """
        Zwraca wartosc przystosowania elementu SSRVE zadanego zbiorem punktow startowych
        :return: Wartość przystosowania w zakresie float <0, 1>
        """
        args = (self.create_starting_points_from_candidate(starting_points))
        img = self.create_ssrve_image(args)
        series_from_ratios, stats = mainFunction(img, ratios=self.ratios, colors=self.colors,
                                                 background=self.background_color_key)

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
        save_to_file('Results/BEST_IN_{0}_POPULATION.png'.format(num_generations), img)

    @abstractmethod
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
                              statistics_file=open("../stats.csv", "w"),
                              individuals_file=open("../individuals.csv", "w"),
                              max_evaluations=1000,
                              neighborhood_size=3,
                              inertia=0.5,  # default 0.5
                              cognitive_rate=1.4,  # default 2.1
                              social_rate=1.4,  # default 2.1
                              )

        # inspyred.ec.analysis.generation_plot(open("stats.csv", "r"))
        # inspyred.ec.analysis.allele_plot("individuals.csv")

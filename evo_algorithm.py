from config import *
from model.fitness_functions import *
from selection.selection_method import SelectionMethod
from model.gen_operators import GeneticOperator
from stats.run_stats import RunStats
from stats.generation_stats import GenerationStats
from output import plotting, excel


class EvoAlgorithm:
    def __init__(self,
                 initial_population: Population,
                 selection_method: SelectionMethod,
                 genetic_operator: GeneticOperator,
                 population_init,
                 param_names: tuple[str]):
        self.population: Population = initial_population
        self.selection_method = selection_method
        self.genetic_operator = genetic_operator
        
        self.param_names = param_names

        self.gen_i = 0
        self.run_stats = RunStats(self.param_names)
        self.prev_gen_stats = None
        self.gen_stats_list = None
        self.has_converged = False
        self.plot_thresholds = None
        
    def run(self, run_i):
        if run_i < RUNS_TO_PLOT:
            self.gen_stats_list = []
            self.plot_thresholds = {}
            for key in [70, 80, 90, 95, 99]:
                self.plot_thresholds[str(key)] = False

        f_avgs = []
        while not self.has_converged and self.gen_i < G:
            gen_stats = self.__calculate_stats_and_evolve(run_i)

            f_avgs.append(gen_stats.f_avg)
            if len(f_avgs) > N_LAST_GENS:
                f_avgs.pop(0)

            self.has_converged = self.population.has_converged(self.param_names)
            self.prev_gen_stats = gen_stats
            self.gen_i += 1

        gen_stats = self.__calculate_final_stats(run_i)
        self.run_stats.NI = self.gen_i
        self.run_stats.has_converged = self.has_converged
        self.run_stats.is_successful = self.__check_success(gen_stats)

        if run_i < RUNS_TO_PLOT:
            # print(f'Generation stats list = {self.gen_stats_list}')
            excel.write_generation_stats(self.gen_stats_list, self.param_names, run_i)
            plotting.plot_generation_stats(self.population, self.param_names, run_i, self.gen_i)
            plotting.plot_run_stats(self.gen_stats_list, self.param_names, run_i)

        return self.run_stats

    def __calculate_stats_and_evolve(self, run_i):
        if run_i < RUNS_TO_PLOT and (self.gen_i < DISTRIBUTIONS_TO_PLOT or self.gen_i % DISTRIBUTION_RATE_TO_PLOT == 0):
            plotting.plot_generation_stats(self.population, self.param_names, run_i, self.gen_i)
        # if run_i < RUNS_TO_PLOT and self.population.is_homogeneous_frac(0.9):
        #     plotting.plot_generation_stats(self.population, self.param_names, run_i, self.gen_i, homogeneous_frac=0.9)
        if run_i < RUNS_TO_PLOT:
            for key in [70, 80, 90, 95, 99]:
                if self.plot_thresholds[str(key)]:
                    continue
                if self.population.is_homogeneous_frac(key/100.):
                    self.plot_thresholds[str(key)] = True
                    plotting.plot_generation_stats(self.population, self.param_names, run_i, 
                                                   self.gen_i, homogeneous_frac=key/100.)
                    excel.write_population_stats(self.population, self.param_names, run_i, 
                                                 self.gen_i, key/100.)

        gen_stats = GenerationStats(self.population, self.param_names, self.selection_method)
        if run_i < RUNS_TO_PLOT:
            self.gen_stats_list.append(gen_stats)

        gen_stats.calculate_stats_before_selection(self.prev_gen_stats)
        self.selection_method.select(self.population)
        gen_stats.calculate_stats_after_selection()
        self.run_stats.update_stats_for_generation(gen_stats, self.gen_i)
        self.genetic_operator.apply(self.population)

        return gen_stats

    def __calculate_final_stats(self, run_i):
        if run_i < RUNS_TO_PLOT and (self.gen_i < DISTRIBUTIONS_TO_PLOT or self.gen_i % DISTRIBUTION_RATE_TO_PLOT == 0):
            plotting.plot_generation_stats(self.population, self.param_names, run_i, self.gen_i)
            
        if run_i < RUNS_TO_PLOT:
            excel.write_population_stats(self.population, self.param_names, run_i, 
                                                 self.gen_i)
            for key in [70, 80, 90, 95, 99]:
                if self.plot_thresholds[str(key)]:
                    continue
                if self.population.is_homogeneous_frac(key/100.):
                    self.plot_thresholds[str(key)] = True
                    plotting.plot_generation_stats(self.population, self.param_names, run_i, 
                                                   self.gen_i, homogeneous_frac=key/100.)
                    excel.write_population_stats(self.population, self.param_names, run_i, 
                                                 self.gen_i, key/100.)

        gen_stats = GenerationStats(self.population, self.param_names, self.selection_method)
        if run_i < RUNS_TO_PLOT:
            self.gen_stats_list.append(gen_stats)

        gen_stats.calculate_stats_before_selection(self.prev_gen_stats)
        self.run_stats.update_final_stats(gen_stats, self.gen_i)

        return gen_stats


    def __check_success(self, gen_stats: GenerationStats):
        if self.param_names[0] == 'FconstALL':
            if self.param_names[2] == 'no_operators':
                return self.population.is_homogenous_100()
            return self.has_converged and self.population.is_homogeneous_frac(90)
        if self.param_names[0] == 'FHD' or self.param_names[0] == 'FH':
            if self.param_names[2] == 'no_operators':
                return self.has_converged and gen_stats.optimal_count == N
            return self.has_converged and gen_stats.optimal_count >= N * 0.9
        else:
            return self.has_converged and self.population.found_close_to_optimal()

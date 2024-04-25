from config import N
from model.population import Population
import numpy as np
from scipy.stats import fisher_exact, kendalltau
from selection.selection_method import SelectionMethod
from selection.rws import ScaledRWS
from selection.sus import ScaledSUS

# stats that are used for graphs
class GenerationStats:

    # static attributes
    num_optimal = None

    def __init__(self, population: Population, param_names: tuple[str], selection_method: SelectionMethod):
        self.population = population
        self.param_names = param_names

        self.f_avg = None
        self.f_std = None
        self.f_best = None
        self.num_of_best = None
        self.optimal_count = None
        # optimal count on previous generation, None for the 1st generation
        self.prev_optimal_count = None
        self.growth_rate = None
        self.difference = None
        self.intensity = None
        self.reproduction_rate = None
        self.loss_of_diversity = None
        # Calculate unique chromosomes separately before and after selection
        self.n_unique_before_selection = None
        self.n_unique_after_selection = None
        self.lose_optimal = False

        # Selection pressure
        self.pr = None
        # Fisher's exact test for selection pressure
        self.P_FET = None
        # Kendall's tau-b test for selection pressure
        self.Kendall_tau = None
        self.init_fitnesses = population.fitnesses
        self.sm = selection_method

    def calculate_stats_before_selection(self, prev_gen_stats):
        self.ids_before_selection = set(self.population.get_ids())
        self.n_unique_before_selection = self.population.get_unique_X()

        if self.param_names[0] != 'FconstALL':
            self.f_avg = self.population.get_fitness_avg()
            self.f_std = self.population.get_fitness_std()
            self.f_best = self.population.get_fitness_max()
            self.num_of_best = self.population.count_fitness_at_least(self.f_best)

            self.prev_optimal_count = GenerationStats.num_optimal
            self.optimal_count = self.population.count_optimal_genotype()
            if GenerationStats.num_optimal is not None and GenerationStats.num_optimal > 0 and self.optimal_count == 0:
                    self.lose_optimal = True
            GenerationStats.num_optimal = self.optimal_count

            if isinstance(self.sm, ScaledRWS) or isinstance(self.sm, ScaledSUS):
                bias = self.sm.b(self.population.fitnesses)
                scaled_fitnesses = np.array([max(self.sm.a*fitness + bias, 0) for fitness in self.population.fitnesses], dtype=np.float64)
                if np.all(scaled_fitnesses == 0):
                    scaled_fitnesses += 0.0001
                self.pr = np.max(scaled_fitnesses) / np.mean(scaled_fitnesses)
            else:
                self.pr = self.f_best / self.f_avg
            
            if not prev_gen_stats:
                self.growth_rate = 1
            else:
                num_of_prev_best = self.population.count_fitness_at_least(prev_gen_stats.f_best)
                self.growth_rate = num_of_prev_best / prev_gen_stats.num_of_best

    def calculate_stats_after_selection(self):
        ids_after_selection = set(self.population.get_ids())
        self.n_unique_after_selection = self.population.get_unique_X()

        self.reproduction_rate = len(ids_after_selection) / N
        self.loss_of_diversity = len([True for id in self.ids_before_selection if id not in ids_after_selection]) / N
        self.ids_before_selection = None

        if self.param_names[0] != 'FconstALL':
            # self.f_avg = self.population.get_fitness_avg()
            # self.f_best = self.population.get_fitness_max()
            # self.pr = self.f_best / self.f_avg

            # Compute Fisher exact test
            fitnesses = list(self.init_fitnesses)
            offspring_counts = []
            is_constant = True
            for id in range(N):
                cnt = 0
                for chr in self.population.chromosomes:
                    if chr.id == id:
                        cnt += 1
                if cnt != 1:
                    is_constant = False
                offspring_counts.append(cnt)
            self.P_FET = self.fisher_exact_test(offspring_counts, fitnesses)
            # it is important to check for constant because Kendall tau returns nan
            if is_constant:
                self.Kendall_tau = 0
            else:
                self.Kendall_tau = kendalltau(np.array(fitnesses), np.array(offspring_counts)).statistic

            self.difference = self.population.get_fitness_avg() - self.f_avg

            if self.f_std == 0:
                self.intensity = 1
            else:
                self.intensity = self.difference / self.f_std

    @staticmethod
    def fisher_exact_test(offspring_counts, fitnesses):
        """
        Compute FET for a given selection
        :param offspring_counts: a list of offspring counts for each chromosome id
        :param fitnesses: a list of chromosome fitnesses
        """
        offspring_counts = np.array(offspring_counts)
        fitnesses = np.array(fitnesses)

        offspring_median = np.median(offspring_counts)
        fitness_median = np.median(fitnesses)

        A = np.sum((fitnesses <= fitness_median) & (offspring_counts <= offspring_median))
        B = np.sum((fitnesses > fitness_median) & (offspring_counts <= offspring_median))
        C = np.sum((fitnesses <= fitness_median) & (offspring_counts > offspring_median))
        D = np.sum((fitnesses > fitness_median) & (offspring_counts > offspring_median))

        contingency_table = np.array([[A, B], [C, D]])

        _, pvalue = fisher_exact(contingency_table, alternative='greater')
        return -np.log10(pvalue)
    
if __name__ == '__main__':
    offspring_counts = [0, 0, 1, 0, 2, 1, 0, 2, 2, 2]
    fitnesses = [0, 1, 1, 2, 3, 4, 5, 5, 7, 9]

    print(f'Traits = {fitnesses}')
    print(f'Offspring = {offspring_counts}')
    print(f'Fisher exact test = {round(GenerationStats.fisher_exact_test(offspring_counts, fitnesses),2)}')
    print(f'Kendall tau-b = {round(kendalltau(np.array(fitnesses), np.array(offspring_counts)).statistic,2)}')

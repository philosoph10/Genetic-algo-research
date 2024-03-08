from config import N
from model.population import Population

# stats that are used for graphs
class GenerationStats:
    def __init__(self, population: Population, param_names: tuple[str]):
        self.population = population
        self.param_names = param_names

        self.f_avg = None
        self.f_std = None
        self.f_best = None
        self.num_of_best = None
        self.optimal_count = None
        self.growth_rate = None
        self.difference = None
        self.intensity = None
        self.reproduction_rate = None
        self.loss_of_diversity = None

    def calculate_stats_before_selection(self, prev_gen_stats):
        self.ids_before_selection = set(self.population.get_ids())

        if self.param_names[0] != 'FconstALL':
            self.f_avg = self.population.get_fitness_avg()
            self.f_std = self.population.get_fitness_std()
            self.f_best = self.population.get_fitness_max()
            self.num_of_best = self.population.count_fitness_at_least(self.f_best)
            self.optimal_count = self.population.count_optimal_genotype()
            
            if not prev_gen_stats:
                self.growth_rate = 1
            else:
                num_of_prev_best = self.population.count_fitness_at_least(prev_gen_stats.f_best)
                self.growth_rate = num_of_prev_best / prev_gen_stats.num_of_best

    def calculate_stats_after_selection(self):
        ids_after_selection = set(self.population.get_ids())
        self.reproduction_rate = len(ids_after_selection) / N
        self.loss_of_diversity = len([True for id in self.ids_before_selection if id not in ids_after_selection]) / N
        self.ids_before_selection = None

        if self.param_names[0] != 'FconstALL':
            self.difference = self.population.get_fitness_avg() - self.f_avg

            if self.f_std == 0:
                self.intensity = 1
            else:
                self.intensity = self.difference / self.f_std